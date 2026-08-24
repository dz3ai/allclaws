"""tinyweb v1.0 test suite — documents current behavior incl. known bugs."""

import threading

import pytest

from tinyweb import create_item, create_user, make_app
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
    import http.client
    from urllib.parse import urlparse

    parsed = urlparse(base)
    conn = http.client.HTTPConnection(parsed.hostname, parsed.port, timeout=10)
    payload = json.dumps(body) if body is not None else None
    headers = {"Content-Type": "application/json"} if payload else {}
    conn.request(method, path, body=payload, headers=headers)
    resp = conn.getresponse()
    data = resp.read()
    conn.close()
    return resp.status, (json.loads(data) if data else None)


import json  # noqa: E402  (used by request helper)


class TestUsers:
    def test_create_and_list(self, base_url):
        status, body = request(base_url, "POST", "/users", {"name": "Ada", "email": "ada@x.io"})
        assert status == 201
        status, body = request(base_url, "GET", "/users")
        assert status == 200 and len(body["users"]) == 1

    def test_get_user_ok(self, base_url):
        _, user = request(base_url, "POST", "/users", {"name": "Ada", "email": "ada@x.io"})
        status, body = request(base_url, "GET", f"/users/{user['id']}")
        assert status == 200 and body["name"] == "Ada"

    def test_get_missing_user_returns_404(self, base_url):
        # FAILS on v1.0: handler sends 200 with an error body (issue-001)
        status, body = request(base_url, "GET", "/users/u-999999")
        assert status == 404
        assert "error" in body

    def test_create_user_validation(self, base_url):
        status, _ = request(base_url, "POST", "/users", {"name": "", "email": "a@b.c"})
        assert status == 400
        status, _ = request(base_url, "POST", "/users", {"name": "A"})
        assert status == 400


class TestItems:
    def test_create_and_list(self, base_url):
        status, item = request(base_url, "POST", "/items", {"name": "Widget", "tag": "hw"})
        assert status == 201
        status, body = request(base_url, "GET", "/items")
        assert status == 200 and [i["id"] for i in body["items"]] == [item["id"]]

    def test_search_is_case_insensitive(self, base_url):
        # FAILS on v1.0: search matches case-sensitively (issue-001)
        request(base_url, "POST", "/items", {"name": "Widget", "tag": "hw"})
        status, body = request(base_url, "GET", "/items?search=widget")
        assert status == 200
        assert len(body["items"]) == 1

    def test_search_empty_returns_all(self, base_url):
        request(base_url, "POST", "/items", {"name": "Widget", "tag": "hw"})
        request(base_url, "POST", "/items", {"name": "Gadget", "tag": "hw"})
        status, body = request(base_url, "GET", "/items")
        assert len(body["items"]) == 2

    def test_search_no_match(self, base_url):
        request(base_url, "POST", "/items", {"name": "Widget", "tag": "hw"})
        status, body = request(base_url, "GET", "/items?search=zzz")
        assert status == 200 and body["items"] == []
