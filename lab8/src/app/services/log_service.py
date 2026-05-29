from pathlib import Path

from app.file_operations import parse_file
from app.logs_parser.my_types import Entry


def load_entries(path: Path) -> list[Entry]:
    return parse_file(path)


def format_entry_summary(entry: Entry, max_uri_length: int = 60) -> str:
    timestamp = entry.ts.isoformat(sep=" ", timespec="seconds") if entry.ts else "-"
    client_ip = str(entry.orig_h) if entry.orig_h else "-"
    method = entry.method or "-"
    status_code = str(entry.status_code.value) if entry.status_code else "-"
    uri = entry.uri or "-"

    if len(uri) > max_uri_length:
        uri = f"{uri[: max_uri_length - 3]}..."

    return f"{timestamp} | {client_ip} | {method} | {status_code} | {uri}"


def build_entry_summaries(entries: list[Entry]) -> list[str]:
    return [format_entry_summary(entry) for entry in entries]
