import os
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import pytest

from pages.task_board import TaskBoardPage


@pytest.fixture(scope="session")
def demo_url():
    override = os.getenv("BASE_URL")
    if override:
        yield override
        return
    handler = partial(
        SimpleHTTPRequestHandler, directory=str(Path(__file__).parent / "demo")
    )
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


@pytest.fixture
def board(page, demo_url):
    return TaskBoardPage(page).open(demo_url)
