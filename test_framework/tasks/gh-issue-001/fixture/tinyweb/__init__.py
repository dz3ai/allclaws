"""tinyweb — a very small stdlib-only web service."""

from .app import make_app, serve
from .models import create_item, create_user, get_item, get_user, search_items
from .routes import RouteTable

__version__ = "1.0.0"

__all__ = [
    "RouteTable",
    "create_item",
    "create_user",
    "get_item",
    "get_user",
    "make_app",
    "search_items",
    "serve",
    "__version__",
]
