import datetime
from pathlib import Path

from app.logs_parser.constants import DETAIL_ENTRY_FIELDS
from app.logs_parser.filters import get_entries_in_time_range
from app.logs_parser.my_types import Entry
from app.services.file_operations import parse_file


def load_entries(path: Path) -> list[Entry]:
    return parse_file(path)


def logs_in_time_range(entries: list[Entry], start: datetime.datetime, end: datetime.datetime):
    return get_entries_in_time_range(entries, start, end)


def min_max_timestamp(entries: list[Entry]):
    timestamps = [entry.ts for entry in entries if entry.ts is not None]
    if not timestamps:
        return None

    first_ts = min(timestamps)
    last_ts = max(timestamps)

    return first_ts, last_ts


def format_entry_summary(entry: Entry, max_uri_length: int = 60) -> str:
    timestamp = entry.ts.isoformat(sep=" ", timespec="seconds") if entry.ts else "-"
    client_ip = str(entry.orig_h) if entry.orig_h else "-"
    method = entry.method or "-"
    status_code = str(entry.status_code.value) if entry.status_code else "-"
    uri = entry.uri or "-"

    if len(uri) > max_uri_length:
        uri = f"{uri[: max_uri_length - 3]}..."

    return f"{timestamp} | {client_ip} | {method} | {status_code} | {uri}"


def format_detail_value(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, datetime.datetime):
        return value.isoformat(sep=" ", timespec="milliseconds")
    if isinstance(value, datetime.date):
        return value.isoformat()
    if isinstance(value, datetime.time):
        return value.isoformat(timespec="milliseconds")
    if hasattr(value, "value"):
        return str(value)
    return str(value)


def build_detail_values(entry: Entry) -> list[str]:
    return [format_detail_value(entry[field_index]) for field_index in DETAIL_ENTRY_FIELDS]


def build_entry_summaries(entries: list[Entry]) -> list[str]:
    return [format_entry_summary(entry) for entry in entries]
