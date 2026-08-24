"""HIDDEN acceptance suite for gh-issue-001 (mounted at scoring time only).

Verifies the two issue-001 defects are fixed and nothing else regressed.
Runs with cwd = the agent's worktree root.
"""

import http.client
import json
import threading
from urllib.parse import urlparse

import pytest

from tinyweb import make_app
from tinyweb import models as models_mod


@pytest.fixture(autouse=True)
def clean_store():
    models_mod.reset()
    yield
    models_mod.reset()


@pytest.fixture()
def base_url():
    srv = make_app("127.0.0.1", 0)
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{srv.server_address[1]}"
    srv.shutdown()
    srv.server_close()


def request(base, method, path, body=None):
    parsed = urlparse(base)
    conn = http.client.HTTPConnection(parsed.hostname, parsed.port, timeout=10)
    payload = json.dumps(body) if body is not None else None
    headers = {"Content-Type": "application/json"} if payload else {}
    conn.request(method, path, body=payload, headers=headers)
    resp = collect_response(conn)
    conn.close()
    return resp


def collect_response(conn):
    resp = conn.getresponse()
    data = resp.read()
    return resp.status, (json.loads(data) if data else None)


class TestUser404:
    def test_missing_user_404(self, base_url):
        status, body = request(base_url, "GET", "/users/u-999999")
        assert status == 404
        assert body and "error" in body

    def test_missing_user_404_body_is_error(self, base_url):
        request(base_url, "POST", "/users", {"name": "Ada", "email": "ada@x.io"})
        status, body = request(base_url, "GET", "/users/u-999999")
        assert status == 404
        assert "error" in body

    def test_existing_user_still_200(self, base_url):
        _, user = request(base_url, "POST", "/users", {"name": "Ada", "email": "ada@x.io"})
        status, body = request(base_url, "GET", f"/users/{user['id']}")
        assert status == 200 and body["name"] == "Ada"


class TestSearchCaseInsensitive:
    def test_lowercase_query_finds_capitalized(self, base_url):
        request(base_url, "POST", "/items", {"name": "Widget", "tag": "hw"})
        status, body = request(base_url, "GET", "/items?search=widget")
        assert status == 200
        assert [i["name"] for i in body["items"]] == ["Widget"]

    def test_uppercase_query_finds_lowercase(self, base_url):
        request(base_url, "POST", "/items", {"name": "widget", "tag": "hw"})
        status, body = request(base_url, "GET", "/items?search=WIDGET")
        assert status == 200
        assert [i["name"] for i in body["items"]] == ["widget"]

    def test_mixed_case_matrix(self, base_url):
        for name in ("Widget", "wIDGET", "Gadget"):
            request(base_url, "POST", "/items", {"name": name, "tag": "hw"})
        for q in ("widget", "WIDGET", "Widget", "wIdGeT"):
            status, body = request(base_url, "GET", f"/items?search={q}")
            assert status == 200
            assert sorted(i["name"] for i in body["items"]) == ["Widget", "wIDGET"], q

    def test_no_match_still_empty(self, base_url):
        request(base_url, "POST", "/items", {"name": "Widget", "tag": "ran"})
        status, body = request(base_url, "GET", "/items?search=zzz")
        assert status == 200 and body["items"] == []

    def test_empty_query_returns_all(self, base_url):
        request(base_url, "POST", "/items", {"name": "A", "tag": "t"})
        request(base_url, "POST", "/items", {"name": "B", "tag": "t"})
        status, body = request(base_url, "GET", "/items")
        assert len(body["items"]) == 2


class TestRegressions:
    def test_create_user(self, base_url):
        status, user = request(base_url, "POST", "/users", {"name": "Ada", "email": "ada@x.io"})
        assert status == 201 and user["id"].startswith("u-")

    def test_list_users(self, base_url):
        request(base_url, "POST", "/users", {"name": "Ada", "email": "ada@x.io"})
        status, body = request(base_url, "GET", "/users")
        assert status == 200 and len(body["users"]) == 1

    def test_create_item(self, base_url):
        status, item = request(base_url, "POST", "/items", {"name": "Widget", "tag": "hw"})
        assert status == 201 and item["id"].startswith("i-")

    def test_user_validation_unchanged(self, base_url):
        status, _ = request(base_url, "POST", "/users", {"name": "A"})
        assert status == 400

    def test_item_validation_unchanged(self, base_url):
        status, _ = request(base_url, "POST", "/items", {"name": "X"})
        assert status == 400
