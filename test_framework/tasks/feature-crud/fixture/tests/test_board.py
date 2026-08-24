"""Existing v1.0 tests — these MUST stay green after the comments feature."""

import json
import threading

import pytest

from taskboard import (
    InvalidTransition,
    TaskNotFound,
    ValidationError,
    create_task,
    delete_task,
    get_task,
    list_tasks,
    make_server,
    move_task,
    update_task,
)
from taskboard import board as board_mod


@pytest.fixture(autouse=True)
def clean_board():
    board_mod.reset()
    yield
    board_mod.reset()


class TestPythonApi:
    def test_create_and_get(self):
        task = create_task("Write tests")
        assert task["title"] == "Write tests"
        assert task["status"] == "todo"
        assert get_task(task["id"])["title"] == "Write tests"

    def test_get_missing(self):
        with pytest.raises(TaskNotFound):
            get_task("t-999999")

    def test_list_filters(self):
        create_task("A", assignee="danny")
        create_task("B", assignee="lee")
        assert len(list_tasks()) == 2
        assert len(list_tasks(assignee="danny")) == 1

    def test_update(self):
        task = create_task("A")
        updated = update_task(task["id"], priority="high")
        assert updated["priority"] == "high"

    def test_update_rejects_unknown_field(self):
        task = create_task("A")
        with pytest.raises(ValidationError):
            update_task(task["id"], bogus=1)

    def test_delete(self):
        task = create_task("A")
        delete_task(task["id"])
        with pytest.raises(TaskNotFound):
            get_task(task["id"])

    def test_move_adjacent_only(self):
        task = create_task("A")
        moved = move_task(task["id"], "doing")
        assert moved["status"] == "doing"
        board_mod.reset()
        task2 = create_task("B")
        with pytest.raises(InvalidTransition):
            move_task(task2["id"], "done")

    def test_validation(self):
        with pytest.raises(ValidationError):
            create_task("")
        with pytest.raises(ValidationError):
            create_task("A", priority="urgent")


class TestHttpApi:
    @pytest.fixture()
    def server(self):
        srv = make_server("127.0.0.1", 0)
        thread = threading.Thread(target=srv.serve_forever, daemon=True)
        thread.start()
        yield f"http://127.0.0.1:{srv.server_address[1]}"
        srv.shutdown()
        srv.server_close()

    def _request(self, base, method, path, body=None):
        import http.client
        from urllib.parse import urlparse

        parsed = urlparse(base)
        conn = http.client.HTTPConnection(parsed.hostname, parsed.port, timeout=10)
        headers = {}
        payload = None
        if body is not None:
            payload = json.dumps(body)
            headers["Content-Type"] = "application/json"
        conn.request(method, path, body=payload, headers=headers)
        resp = conn.getresponse()
        data = resp.read()
        conn.close()
        parsed_body = json.loads(data) if data else None
        return resp.status, parsed_body

    def test_task_lifecycle(self, server):
        status, body = self._request(server, "POST", "/tasks", {"title": "HTTP task"})
        assert status == 201
        task_id = body["id"]

        status, body = self._request(server, "GET", "/tasks")
        assert status == 200 and len(body["tasks"]) == 1

        status, body = self._request(server, "GET", f"/tasks/{task_id}")
        assert status == 200 and body["title"] == "HTTP task"

        status, body = self._request(server, "PUT", f"/tasks/{task_id}", {"priority": "high"})
        assert status == 200 and body["priority"] == "high"

        status, body = self._request(server, "POST", f"/tasks/{task_id}/move", {"to": "doing"})
        assert status == 200 and body["status"] == "doing"

        status, _ = self._request(server, "DELETE", f"/tasks/{task_id}")
        assert status == 204

        status, _ = self._request(server, "GET", f"/tasks/{task_id}")
        assert status == 404

    def test_error_paths(self, server):
        status, body = self._request(server, "GET", "/tasks/t-999999")
        assert status == 404
        status, body = self._request(server, "POST", "/tasks", {})
        assert status == 400
        status, body = self._request(server, "POST", "/tasks", {"title": "X", "priority": "nope"})
        assert status == 400
