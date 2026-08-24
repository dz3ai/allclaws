"""taskboard.storage — JSON persistence for the board state."""

import json
import os

from . import board


def save_board(path):
    """Persist tasks + comments to `path` as JSON."""
    tasks = {tid: dict(t) for tid, t in board.all_tasks_raw().items()}
    comments = {tid: [dict(c) for c in clist] for tid, clist in board.all_comments_raw().items()}
    payload = {"version": 1, "tasks": tasks, "comments": comments}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True)


def load_board(path):
    """Restore board state from a JSON file written by save_board."""
    with open(path, encoding="utf-8") as fh:
        payload = json.load(fh)
    tasks = payload.get("tasks", {})
    comments = payload.get("comments", {})
    next_task = max((int(t["id"][2:]) for t in tasks.values()), default=0) + 1
    next_comment = 0
    for clist in comments.values():
        for c in clist:
            next_comment = max(next_comment, int(c["id"][2:]))
    next_comment += 1
    board.reset(
        next_task_id=next_task,
        next_comment_id=next_comment,
        tasks=tasks,
        comments=comments,
    )
    return payload
