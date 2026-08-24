# taskboard — kanban task board service

A small, dependency-free (stdlib-only) task board with columns, JSON
persistence, and a REST-ish HTTP API built on `http.server`.

## Existing functionality (v1.0)

### Python API (exported from `taskboard`)

| Function | Behavior |
|---|---|
| `list_tasks(status=None, assignee=None)` | Tasks filtered by status/assignee |
| `get_task(task_id)` | One task or raises `TaskNotFound` |
| `create_task(title, assignee=None, priority="medium")` | New task in `todo` column |
| `update_task(task_id, **fields)` | Update title/assignee/priority/status |
| `delete_task(task_id)` | Remove a task |
| `move_task(task_id, to_column)` | `todo` → `doing` → `done` (adjacent moves only) |
| `make_server(host, port)` | Ready-to-serve `ThreadingHTTPServer` |
| `serve(host="127.0.0.1", port=8765)` | Serve until KeyboardInterrupt |

Exceptions: `TaskNotFound`, `InvalidTransition`, `ValidationError`.

### HTTP API

```
GET    /tasks                 → 200 {"tasks": [...]}
GET    /tasks/<id>            → 200 task object | 404
POST   /tasks                 {"title": str, "assignee"?: str, "priority"?: str} → 201 task
PUT    /tasks/<id>            {"title"?/"assignee"?/"priority"?/"status"?} → 200 task | 404 | 400
DELETE /tasks/<id>            → 204 | 404
POST   /tasks/<id>/move      {"to": "doing"} → 200 task | 404 | 400
```

Priorities: `low`, `medium`, `high` (invalid → 400 `ValidationError`).
Columns: `todo`, `doing`, `done` — moves must be adjacent (`todo→done`
directly is an `InvalidTransition` → 400).

## Feature request

See `feature-request.md` — a comments feature is being requested. This README
documents the *current* API only; the feature request is the source of truth
for the new endpoints.

## Development

```
/usr/bin/python3 -m pytest tests/ -q
```

No third-party dependencies — see requirements.txt.
