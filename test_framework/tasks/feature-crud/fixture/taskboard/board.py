"""taskboard.board — in-memory board state + task/comment operations."""

import itertools
import re
from datetime import datetime, timezone

COLUMNS = ("todo", "doing", "done")
PRIORITIES = ("low", "medium", "high")

_task_ids = itertools.count(1)
_comment_ids = itertools.count(1)

# module-level board state (single-board service)
_tasks: dict = {}
_comments: dict = {}  # task_id -> list[comment dict]


class TaskNotFound(LookupError):
    pass


class CommentNotFound(LookupError):
    pass


class InvalidTransition(ValueError):
    pass


class ValidationError(ValueError):
    pass


def _utcnow_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _validate_title(title):
    if not isinstance(title, str) or not title.strip():
        raise ValidationError("title must be a non-empty string")
    if len(title) > 200:
        raise ValidationError("title must be at most 200 chars")


def _validate_priority(priority):
    if priority not in PRIORITIES:
        raise ValidationError(f"priority must be one of {PRIORITIES}")


def _validate_status(status):
    if status not in COLUMNS:
        raise ValidationError(f"status must be one of {COLUMNS}")


# ---------------------------------------------------------------- tasks

def list_tasks(status=None, assignee=None):
    """All tasks, optionally filtered by status and/or assignee."""
    rows = list(_tasks.values())
    if status is not None:
        _validate_status(status)
        rows = [t for t in rows if t["status"] == status]
    if assignee is not None:
        rows = [t for t in rows if t.get("assignee") == assignee]
    return [dict(t) for t in rows]


def get_task(task_id):
    try:
        return dict(_tasks[task_id])
    except KeyError:
        raise TaskNotFound(task_id) from None


def create_task(title, assignee=None, priority="medium"):
    _validate_title(title)
    _validate_priority(priority)
    task_id = f"t-{next(_task_ids):06d}"
    task = {
        "id": task_id,
        "title": title,
        "assignee": assignee,
        "priority": priority,
        "status": COLUMNS[0],
        "created_at": _utcnow_iso(),
    }
    _tasks[task_id] = task
    return dict(task)


def update_task(task_id, **fields):
    if task_id not in _tasks:
        raise TaskNotFound(task_id)
    task = _tasks[task_id]
    if "title" in fields:
        _validate_title(fields["title"])
    if "priority" in fields:
        _validate_priority(fields["priority"])
    if "status" in fields:
        _validate_status(fields["status"])
    for key, value in fields.items():
        if key not in ("title", "assignee", "priority", "status"):
            raise ValidationError(f"unknown field: {key}")
        task[key] = value
    return dict(task)


def delete_task(task_id):
    if task_id not in _tasks:
        raise TaskNotFound(task_id)
    del _tasks[task_id]
    _comments.pop(task_id, None)


def move_task(task_id, to_column):
    if task_id not in _tasks:
        raise TaskNotFound(task_id)
    if to_column not in COLUMNS:
        raise ValidationError(f"to_column must be one of {COLUMNS}")
    task = _tasks[task_id]
    current = task["status"]
    if COLUMNS.index(to_column) - COLUMNS.index(current) != 1:
        raise InvalidTransition(f"cannot move {current} -> {to_column}")
    task["status"] = to_column
    return dict(task)


# ------------------------------------------------------------- internals

def all_tasks_raw():
    """Internal: live dict references (for storage layer)."""
    return _tasks


def all_comments_raw():
    """Internal: live comments mapping (for storage layer)."""
    return _comments


def reset(next_task_id=1, next_comment_id=1, tasks=None, comments=None):
    """Internal: reset/restore board state (used by storage + tests)."""
    global _tasks, _comments
    _tasks = dict(tasks or {})
    _comments = dict(comments or {})
    _task_ids = itertools.count(next_task_id)
    _comment_ids = itertools.count(next_comment_id)
