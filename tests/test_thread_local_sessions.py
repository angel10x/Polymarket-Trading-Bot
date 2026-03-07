"""
Unit tests for thread-local HTTP sessions.
"""

import queue
import threading
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.client import ApiClient
from src.gamma_client import GammaClient


def _session_id(client, out_queue: queue.Queue) -> None:
    out_queue.put(id(client.session))


def test_api_client_thread_local_session():
    client = ApiClient(base_url="https://example.com")
    main_id = id(client.session)

    out_queue = queue.Queue()
    worker = threading.Thread(target=_session_id, args=(client, out_queue))
    worker.start()
    worker.join()

    thread_id = out_queue.get()
    assert main_id != thread_id


def test_gamma_client_thread_local_session():
    client = GammaClient()
    main_id = id(client.session)

    out_queue = queue.Queue()
    worker = threading.Thread(target=_session_id, args=(client, out_queue))
    worker.start()
    worker.join()

    thread_id = out_queue.get()
    assert main_id != thread_id
