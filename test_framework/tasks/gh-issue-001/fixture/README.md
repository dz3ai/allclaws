# tinyweb — a very small web service

A stdlib-only (http.server) JSON web service with an in-memory store, used
for bug-fixing exercises. No third-party dependencies (see requirements.txt).

## API

```
GET    /users                 → 200 {"users": [...]}
POST   /users                 {"name": str, "email": str} → 201 user
GET    /users/<id>            → 200 user | 404 when the id does not exist
GET    /items                 → 200 {"items": [...]}
GET    /items?search=<q>      → 200 {"items": [...]} — case-INSENSITIVE substring
                                match over item names; empty/missing q returns all
POST   /items                 {"name": str, "tag": str} → 201 item
```

User object: `{"id": "u-000001", "name": str, "email": str}`.
Item object: `{"id": "i-000001", "name": str, "tag": str}`.

Errors are JSON: `{"error": "<message>"}` with a meaningful status code.

## Development

```
/usr/bin/python3 -m pytest tests/ -q
```

## Layout

```
tinyweb/
├── __init__.py   # public exports
├── app.py        # HTTP handler + make_app/serve
├── routes.py     # route table + request dispatch
└── models.py     # in-memory stores
```
