"""tinyweb.routes — route table + request dispatch."""

import re

from . import models


class RouteTable:
    """Thin route registry (kept for programmatic API users).

    `dispatch()` uses the module-level ROUTES list directly; this class
    exists so the documented `tinyweb.RouteTable` export stays importable.
    """

    def __init__(self):
        self._routes = []

    def add(self, pattern, method, handler, body_mode=None):
        compiled = re.compile(pattern) if isinstance(pattern, str) else pattern
        self._routes.append((compiled, method.upper(), handler, body_mode))

    def resolve(self, method, path):
        """Return (handler, match) or None."""
        for compiled, m, handler, body_mode in self._routes:
            match = compiled.match(path)
            if match and m == method.upper():
                return handler, match
        return None


class ApiError(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status
        self.message = message


def _user_or_error(uid):
    try:
        return models.get_user(uid)
    except models.UserNotFound:
        # BUG (issue-001): should be 404, not 200-with-error-body
        raise ApiError(200, f"user {uid} not found") from None


def handle_list_users():
    return 200, {"users": models.list_users()}


def handle_create_user(body):
    if "name" not in body or "email" not in body:
        raise ApiError(400, "name and email are required")
    try:
        user = models.create_user(body["name"], body["email"])
    except ValueError as e:
        raise ApiError(400, str(e)) from None
    return 201, user


def handle_get_user(uid):
    return 200, _user_or_error(uid)


def handle_list_items(query):
    search = (query or {}).get("search", [""])
    results = models.search_items(search[0] if search else "")
    return 200, {"items": results}


def handle_create_item(body):
    if "name" not in body or "tag" not in body:
        raise ApiError(400, "name and tag are required")
    try:
        item = models.create_item(body["name"], body["tag"])
    except ValueError as e:
        raise ApiError(400, str(e)) from None
    return 201, item


ROUTES = [
    (re.compile(r"^/users/?$"), "GET", handle_list_users, None),
    (re.compile(r"^/users/?$"), "POST", handle_create_user, "json"),
    (re.compile(r"^/users/([^/]+)/?$"), "GET", handle_get_user, None),
    (re.compile(r"^/items/?$"), "GET", handle_list_items, "query"),
    (re.compile(r"^/items/?$"), "POST", handle_create_item, "json"),
]


def dispatch(method, path, query=None, body=None):
    """Route a request; returns (status, payload) or raises ApiError."""
    for pattern, m, handler, body_mode in ROUTES:
        match = pattern.match(path)
        if match and m == method:
            kwargs = {}
            if body_mode == "json":
                kwargs["body"] = body or {}
            if body_mode == "query":
                kwargs["query"] = query or {}
            return handler(*match.groups(), **kwargs)
    raise ApiError(404, f"no route for {method} {path}")
