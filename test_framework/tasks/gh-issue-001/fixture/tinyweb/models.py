"""tinyweb.models — in-memory stores for users and items."""

import itertools

_user_ids = itertools.count(1)
_item_ids = itertools.count(1)

_users: dict = {}
_items: dict = {}


class UserNotFound(LookupError):
    pass


class ItemNotFound(LookupError):
    pass


def reset(users=None, items=None):
    """Internal: reset/restore store state (used by tests)."""
    global _users, _items, _user_ids, _item_ids
    _users = dict(users or {})
    _items = dict(items or {})
    _user_ids = itertools.count(
        max((int(u["id"][2:]) for u in _users.values()), default=0) + 1
    )
    _item_ids = itertools.count(
        max((int(i["id"][2:]) for i in _items.values()), default=0) + 1
    )


def list_users():
    return [dict(u) for u in _users.values()]


def create_user(name, email):
    if not isinstance(name, str) or not name.strip():
        raise ValueError("name must be a non-empty string")
    if not isinstance(email, str) or "@" not in email:
        raise ValueError("email must contain @")
    uid = f"u-{next(_user_ids):06d}"
    user = {"id": uid, "name": name, "email": email}
    _users[uid] = user
    return dict(user)


def get_user(uid):
    """Return the user dict or raise UserNotFound."""
    try:
        return dict(_users[uid])
    except KeyError:
        raise UserNotFound(uid) from None


def list_items():
    return [dict(i) for i in _items.values()]


def create_item(name, tag):
    if not isinstance(name, str) or not name.strip():
        raise ValueError("name must be a non-empty string")
    iid = f"i-{next(_item_ids):06d}"
    item = {"id": iid, "name": name, "tag": tag}
    _items[iid] = item
    return dict(item)


def get_item(iid):
    try:
        return dict(_items[iid])
    except KeyError:
        raise ItemNotFound(iid) from None


def search_items(query):
    """Case-insensitive substring search over item names (per README).

    BUG (issue-001): current implementation matches case-sensitively and
    scans keywords×items (quadratic). Should be case-insensitive, linear.
    """
    query = (query or "").strip()
    if not query:
        return list_items()
    results = []
    keywords = query.split()
    for item in _items.values():
        matched = 0
        for keyword in keywords:
            for word in item["name"].split():
                if keyword in word:
                    matched += 1
                    break
        if matched == len(keywords):
            results.append(dict(item))
    return results
