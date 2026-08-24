# Feature: comments on tasks

## Summary

Team members need to discuss tasks. Add threaded-free flat comments to tasks,
exposed through both the HTTP API and the Python API.

## HTTP API (new)

```
POST   /tasks/<id>/comments           {"author": str, "body": str}  → 201 comment | 400 | 404
GET    /tasks/<id>/comments           → 200 {"comments": [...]} ordered by created_at ascending | 404
DELETE /tasks/<id>/comments/<cid>     → 204 | 404 (task or comment)
```

## Comment object shape

```json
{
  "id": "c-000001",
  "task_id": "t-000001",
  "author": "danny",
  "body": "looks good to me",
  "created_at": "2026-01-01T00:00:00Z"
}
```

- `id`: unique comment id, pattern `c-` + 6 digits
- `created_at`: ISO 8601 UTC timestamp string ending in `Z`

## Validation rules

- `author`: non-empty string, at most 80 chars → else **400**
- `body`: 1-2000 chars → else **400**
- comment on a missing task → **404**
- delete of a missing comment (or missing task) → **404**
- malformed JSON body → **400**

## Python API (new, exported from `taskboard`)

| Function | Behavior |
|---|---|
| `add_comment(task_id, author, body)` | Create comment, returns comment dict; raises `TaskNotFound` / `ValidationError` |
| `list_comments(task_id)` | Comments ordered by `created_at` ascending; raises `TaskNotFound` |
| `delete_comment(task_id, comment_id)` | Remove comment; raises `TaskNotFound` / `CommentNotFound` |

New exception: `CommentNotFound`.

## Notes

- Comments are in-memory + persisted via the storage layer (same lifecycle
  as tasks).
- No third-party dependencies. Follow existing code style.
- All existing tests must keep passing.
