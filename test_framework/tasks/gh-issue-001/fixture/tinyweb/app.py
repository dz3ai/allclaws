"""tinyweb.app — HTTP plumbing on http.server."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .routes import ApiError, dispatch


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

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

    def _handle(self, method):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        try:
            body = self._read_json() if method in ("POST", "PUT") else None
            status, payload = dispatch(method, parsed.path, query=query, body=body)
            self._send(status, payload)
        except ApiError as e:
            self._send(e.status, {"error": e.message})
        except Exception as e:  # noqa: BLE001 — API boundary
            self._send(500, {"error": f"internal error: {e}"})

    def do_GET(self):
        self._handle("GET")

    def do_POST(self):
        self._handle("POST")


def make_app(host="127.0.0.1", port=8765):
    """Build a ready-to-serve ThreadingHTTPServer."""
    return ThreadingHTTPServer((host, port), Handler)


def serve(host="127.0.0.1", port=8765):
    server = make_app(host, port)
    print(f"tinyweb listening on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
