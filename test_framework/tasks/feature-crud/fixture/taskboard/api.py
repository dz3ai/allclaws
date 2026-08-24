"""taskboard.api — REST-ish HTTP API on http.server (existing v1.0 routes)."""

import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from . import board


class ApiError(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status
        self.message = message


def _task_or_404(task_id):
    try:
        return board.get_task(task_id)
    except board.TaskNotFound:
        raise ApiError(404, f"task {task_id} not found") from None


class Handler(BaseHTTPRequestHandler):
    """Routes: GET/POST /tasks, GET/PUT/DELETE /tasks/<id>, POST /tasks/<id>/move."""

    def log_message(self, format, *args):  # silence default stderr logging
        pass

    # ------------------------------------------------------------- helpers

    def _send(self, status, payload=None):
        body = b"" if payload is None else json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if payload is not None:
            self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        if not raw:
            raise ApiError(400, "empty request body")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            raise ApiError(400, "malformed JSON body") from None
        if not isinstance(data, dict):
            raise ApiError(400, "JSON body must be an object")
        return data

    # ------------------------------------------------------------- routing

    def do_GET(self):
        self._dispatch("GET")

    def do_POST(self):
        self._dispatch("POST")

    def do_PUT(self):
        self._dispatch("PUT")

    def do_DELETE(self):
        self._dispatch("DELETE")

    def _dispatch(self, method):
        try:
            handler, match = self._route(method, self.path)
            status, payload = handler(match)
            self._send(status, payload)
        except ApiError as e:
            self._send(e.status, {"error": e.message})
        except board.ValidationError as e:
            self._send(400, {"error": str(e)})
        except board.TaskNotFound as e:
            self._send(404, {"error": f"task {e} not found"})
        except Exception as e:  # noqa: BLE001 — API boundary
            self._send(500, {"error": f"internal error: {e}"})

    def _route(self, method, path):
        path = path.split("?", 1)[0].rstrip("/") or "/"

        if path == "/tasks":
            if method == "GET":
                return self._list_tasks, None
            if method == "POST":
                return self._create_task, None

        match = re.fullmatch(r"/tasks/([^/]+)", path)
        if match:
            tid = match.group(1)
            if method == "GET":
                return self._get_task, tid
            if method == "PUT":
                return self._update_task, tid
            if method == "DELETE":
                return self._delete_task, tid

        match = re.fullmatch(r"/tasks/([^/]+)/move", path)
        if match and method == "POST":
            return self._move_task, match.group(1)

        raise ApiError(404, f"no route for {method} {path}")

    # ------------------------------------------------------------ handlers

    def _list_tasks(self, _):
        return 200, {"tasks": board.list_tasks()}

    def _create_task(self, _):
        data = self._read_json()
        if "title" not in data:
            raise ApiError(400, "title is required")
        try:
            task = board.create_task(
                title=data["title"],
                assignee=data.get("assignee"),
                priority=data.get("priority", "medium"),
            )
        except board.ValidationError as e:
            raise ApiError(400, str(e)) from None
        return 201, task

    def _get_task(self, tid):
        return 200, _task_or_404(tid)

    def _update_task(self, tid):
        _task_or_404(tid)
        data = self._read_json()
        fields = {}
        for key in ("title", "assignee", "priority", "status"):
            if key in data:
                fields[key] = data[key]
        try:
            task = board.update_task(tid, **fields)
        except board.TaskNotFound:
            raise ApiError(404, f"task {tid} not found") from None
        except board.ValidationError as e:
            raise ApiError(400, str(e)) from None
        returns = (200, task)
        return returns

    def _delete_task(self, tid):
        _task_or_404(tid)
        board.delete_task(tid)
        return 204, None

    def _move_task(self, tid):
        _task_or_404(tid)
        data = self._read_json()
        if "to" not in data:
            raise ApiError(400, "'to' is required")
        try:
            task = board.move_task(tid, data["to"])
        except board.TaskNotFound:
            raise ApiError(404, f"task {tid} not found") from None
        except (board.ValidationError, board.InvalidTransition) as e:
            raise ApiError(400, str(e)) from None
        return 200, task


def make_server(host="127.0.0.1", port=8765):
    """Build a ready-to-serve ThreadingHTTPServer."""
    return ThreadingHTTPServer((host, port), Handler)


def serve(host="127.0.0.1", port=8765):
    """Serve until interrupted."""
    server = make_server(host, port)
    print(f"taskboard listening on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
