from pathlib import Path

import pytest

from app.converters import read_log
from app.types import Entry

LOG_PATH = Path(__file__).parent.parent / "data" / "http_first_100k.log"


@pytest.fixture(scope="session")
def log() -> list[Entry]:
    with LOG_PATH.open() as f:
        import sys
        old_stdin = sys.stdin
        sys.stdin = f
        result = read_log()
        sys.stdin = old_stdin
    return result
