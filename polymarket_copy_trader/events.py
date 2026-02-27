"""Event sink for UI: stream "his" vs "my" tasks and log lines."""

import logging
import queue
from typing import Any, Callable

# Optional queue for UI: items are ("task", who, payload) or ("log", record).
# UI sets this before starting the runner; runner/trader push to it when present.
_ui_queue: queue.Queue[tuple[str, Any, ...]] | None = None


def set_ui_queue(q: queue.Queue[tuple[str, Any, ...]] | None) -> None:
    """Set the global queue for UI events. Call with None to clear."""
    global _ui_queue
    _ui_queue = q


def get_ui_queue() -> queue.Queue[tuple[str, Any, ...]] | None:
    """Return the current UI queue, if any."""
    return _ui_queue


def emit_task(who: str, change: dict[str, Any], result: Any = None) -> None:
    """
    Emit a task line for the UI.
    who: "his" (copied trader) or "mine" (our copy).
    change: dict with type (BUY/SELL), size, title, slug, etc.
    result: for "mine", the order object or None if failed.
    """
    q = get_ui_queue()
    if q is not None:
        try:
            q.put_nowait(("task", who, change, result))
        except queue.Full:
            pass


def emit_log(record: logging.LogRecord) -> None:
    """Emit a log record for the UI to display."""
    q = get_ui_queue()
    if q is not None:
        try:
            q.put_nowait(("log", record))
        except queue.Full:
            pass
