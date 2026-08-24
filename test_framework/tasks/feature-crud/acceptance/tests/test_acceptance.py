"""HIDDEN acceptance suite for feature-crud (mounted at scoring time only).

Exercises the comments feature exactly as specified in feature-request.md:
HTTP lifecycle over a live server (ephemeral port), Python API parity,
validation 400s, 404s, ordering, ISO 8601 created_at, and regression on the
existing task endpoints. Runs with cwd = agent's worktree root.
"""

import http.client
import json
import re
import threading
from urllib.parse import urlparse

import pytest

from taskboard import (
    CommentNotFound,
    TaskNotFound,
    ValidationError,
    add_comment,
    create_task,
    delete_comment,
    list_comments,
    list_tasks,
)
from taskboard import board as board_mod


@pytest.fixture(autouse=True)
def clean_board():
    board_mod.reset()
    yield
    board_mod.reset()


ISO_Z = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


# ------------------------------------------------------------------ helpers

@pytest.fixture(scope="class")
def base_url(request):
    from taskboard import make_server

    srv = make_server("127.0.0.1", 0)
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{srv.server_address[1]}"
    request.cls.base_url = url
    yield url
    srv.shutdown()
    srv.server_close()


@pytest.fixture()
def task_id():
    t = create_task("Acceptance task")
    return t["id"]


def request(base, method, path, body=None, raw_body=None):
    parsed = urlparse(base)
    conn = http.client.HTTPConnection(parsed.hostname, parsed.port, timeout=10)
    headers = {}
    payload = None
    if raw_body is not None:
        payload = raw_body
        headers["Content-Type"] = "application/json"
    elif body is not None:
        payload = json.dumps(body)
        headers["Content-Type"] = "application/json"
    conn.request(method, path, body=payload, headers=headers)
    resp = conn.getresponse()
    data = resp.read()
    conn.close()
    return resp.status, (json.loads(data) if data else None)


@pytest.mark.usefixtures("base_url")
class TestHttpCommentsLifecycle:
    def test_full_crud_lifecycle(self, base_url, task_id):
        # POST creates → 201 + shape
        status, comment = request(
            base_url, "POST", f"/tasks/{task_id}/comments",
            {"author": "danny", "body": "looks good"},
        )
        assert status == 201, comment
        assert comment["author"] == "danny"
        assert comment["body"] == "looks good"
        assert comment["task_id"] == task_id
        assert re.fullmatch(r"c-\d{6}", comment["id"]), comment["id"]
        assert ISO_Z.match(comment["created_at"]), comment["created_at"]

        # GET lists → 200, ordered
        status, body = request(base_url, "GET", f"/tasks/{task_id}/comments")
        assert status == 200
        assert [c["id"] for c in body["comments"]] == [comment["id"]]

        # DELETE → 204, then listing is empty and re-DELETE is 404
        status, _ = request(base_url, "DELETE", f"/tasks/{task_id}/comments/{comment['id']}")
        assert status == 204
        status, body = request(base_url, "GET", f"/tasks/{task_id}/comments")
        assert status == 200 and body["comments"] == []
        status, _ = request(base_url, "DELETE", f"/tasks/{task_id}/comments/{comment['id']}")
        assert status == 404

    def test_ordering_two_comments(self, base_url, task_id):
        ids = []
        for i in range(2):
            status, c = request(
                base_url, "POST", f"/tasks/{task_id}/comments",
                {"author": "a", "body": f"c{i}"},
            )
            assert status == 201
            ids.append(c)
        status, body = request(base_url, "GET", f"/tasks/{task_id}/comments")
        times = [c["created_at"] for c in body["comments"]]
        assert times == sorted(times), times


@pytest.mark.usefixtures("base_url")
class TestHttpValidation:
    def test_body_empty_rejected(self, base_url, task_id):
        status, body = request(base_url, "POST", f"/tasks/{task_id}/comments", {"author": "a", "body": ""})
        assert status == 400

    def test_body_too_long_rejected(self, base_url, task_id):
        status, _ = request(base_url, "POST", f"/tasks/{task_id}/comments", {"author": "a", "body": "x" * 2001})
        assert status == 400

    def test_body_exactly_2000_ok(self, base_url, task_id):
        status, _ = request(base_url, "POST", f"/tasks/{task_id}/comments", {"author": "a", "body": "x" * 2000})
        assert status == 201

    def test_author_empty_rejected(self, base_url, task_id):
        status, _ = request(base_url, "POST", f"/tasks/{task_id}/comments", {"author": "", "body": "hi"})
        assert status == 400

    def test_author_too_long_rejected(self, base_url, task_id):
        status, _ = request(base_url, "POST", f"/tasks/{task_id}/comments", {"author": "a" * 81, "body": "hi"})
        assert status == 400

    def test_missing_task_404(self, base_url):
        status, _ = request(base_url, "POST", "/tasks/t-999999/comments", {"author": "a", "body": "hi"})
        assert status == 404
        status, _ = request(base_url, "GET", "/tasks/t-999999/comments")
        assert status == 404

    def test_malformed_json_400(self, base_url, task_id):
        status, _ = request(base_url, "POST", f"/tasks/{task_id}/comments", raw_body=b"{not json")
        assert status == 400


@pytest.mark.usefixtures("base_url")
class TestHttpRegression:
    def test_existing_task_endpoints_untouched(self, base_url):
        status, task = request(base_url, "POST", "/tasks", {"title": "Regression"})
        assert status == 201
        status, body = request(base_url, "GET", "/tasks")
        assert status == 200 and len(body["tasks"]) >= 1
        status, body = request(base_url, "PUT", f"/tasks/{task['id']}", {"priority": "high"})
        assert status == 200 and body["priority"] == "high"
        status, body = request(base_url, "POST", f"/tasks/{task['id']}/move", {"to": "doing"})
        assert status == 200 and body["status"] == "doing"
        status, _ = request(base_url, "DELETE", f"/tasks/{task_id_reg(task)}")
        assert status == 204


def task_id_reg(task):
    return task["id"]


class TestPythonApi:
    def test_add_list_delete(self, task_id):
        c1 = add_comment(task_id, "danny", "first")
        c2 = add_comment(task_id, "lee", "second")
        assert c1["task_id"] == task_id and c2["task_id"] == task_id
        listed = list_comments(task_id)
        assert [c["id"] for c in listed] == [c1["id"], c2["id"]]
        delete_comment(task_id, c1["id"])
        assert [c["id"] for c in list_comments(task_id)] == [c2["id"]]

    def test_exceptions(self, task_id):
        with pytest.raises(TaskNotFound):
            add_comment("t-999999", "a", "hi")
        with pytest.raises(TaskNotFound):
            list_comments("t-999999")
        c = add_comment(task_id, "a", "hi")
        with pytest.raises(CommentNotFound):
            delete_comment(task_id, "c-999999")
        with pytest.raises(ValidationError):
            add_comment(task_id, "", "hi")
        with pytest.raises(ValidationError):
            add_comment(task_id, "a", "x" * 2001)

    def test_comments_die_with_task(self, task_id):
        add_comment(task_id, "a", "bye")
        from taskboard import delete_task

        delete_task(task_id)
        with pytest.raises(TaskNotFound):
            list_comments(task_id)

    def test_exported_from_package(self):
        import taskboard

        for name in ("add_comment", "list_comments", "delete_comment", "CommentNotFound"):
            assert hasattr(taskboard, name), f"taskboard.{name} not exported"


class TestPersistence:
    def test_comments_survive_roundtrip(self, task_id, tmp_path):
        from taskboard import load_board, save_board

        add_comment(task_id, "danny", "persisted")
        path = tmp_path / "board.json"
        save_board(str(path))
        board_mod.reset()
        load_board(str(path))
        listed = list_comments(task_id)
        assert [c["body"] for c in listed] == ["persisted"]
        # and the next comment id does not collide
        c2 = add_comment(task_id, "danny", "after reload")
        assert c2["id"] != listed[0]["id"]
