"""
HTTP Utilities - Shared HTTP session helpers.

Provides a thread-local requests.Session mixin to avoid cross-thread reuse.
"""

import threading
from typing import Any

import requests


class ThreadLocalSessionMixin:
    """
    Mixin providing a thread-local requests.Session.

    Each thread gets its own Session instance to keep connections isolated.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._session_local = threading.local()
        super().__init__(*args, **kwargs)

    def _get_session(self) -> requests.Session:
        """Get a thread-local session to avoid cross-thread reuse."""
        session = getattr(self._session_local, "session", None)
        if session is None:
            session = requests.Session()
            self._session_local.session = session
        return session

    @property
    def session(self) -> requests.Session:
        """Expose the thread-local session for internal use."""
        return self._get_session()
