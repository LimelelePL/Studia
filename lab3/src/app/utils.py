import io
import sys

from app.my_types import EntryDict


def format_stream_utf8() -> None:
    if isinstance(sys.stdin, io.TextIOWrapper):
        sys.stdin.reconfigure(encoding="utf-8")

    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")


def get_num_of_requests(session: list[EntryDict]) -> int:
    return len(session)
