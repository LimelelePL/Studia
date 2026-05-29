import datetime
import sys
from http import HTTPStatus
from ipaddress import IPv4Address
from typing import Any

from app.logs_parser.constants import EMPTY_ENTRY, EMPTY_FIELD, RAW_LOG_FIELD_INDEXES
from app.logs_parser.my_types import Entry, EntryDict


def _to_datetime(value: Any) -> datetime.datetime | None:
    try:
        return datetime.datetime.fromtimestamp(float(value))
    except (ValueError, OSError, TypeError):
        return None


def _to_timezone(value: Any) -> str | None:
    try:
        aware_dt = datetime.datetime.fromtimestamp(float(value), tz=datetime.UTC).astimezone()
        if aware_dt.dst():
            return "CEST"
        return "CET"
    except (ValueError, OSError, TypeError):
        return None


def _to_int(value: Any) -> int | None:
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def _to_http_status(value: Any) -> HTTPStatus | None:
    try:
        return HTTPStatus(int(value))
    except (ValueError, TypeError):
        return None


def _to_ip(value: Any) -> IPv4Address | None:
    try:
        return IPv4Address(value)
    except (ValueError, TypeError):
        return None


def _normalize_raw_entry(raw_fields: list[str]) -> Entry:
    normalized_entry = [None if x == EMPTY_FIELD else x for x in raw_fields]
    ts, uid, orig_h, orig_p, resp_h, resp_p, method, host, uri, status_code, size = normalized_entry
    parsed_ts = _to_datetime(ts)

    return Entry(
        ts=parsed_ts,
        uid=uid,
        orig_h=_to_ip(orig_h),
        orig_p=_to_int(orig_p),
        resp_h=_to_ip(resp_h),
        resp_p=_to_int(resp_p),
        method=method,
        host=_to_ip(host),
        uri=uri,
        status_code=_to_http_status(status_code),
        size=_to_int(size),
        date=parsed_ts.date() if parsed_ts else None,
        time=parsed_ts.time() if parsed_ts else None,
        timezone=_to_timezone(ts),
    )


def _extract_raw_entry_fields(raw_log_line: str) -> list[str]:
    fields = raw_log_line.split("\t")
    return [fields[i] for i in RAW_LOG_FIELD_INDEXES]


def read_log() -> list[Entry]:
    log: list[Entry] = []
    for line in sys.stdin:
        if raw_log_line := line.strip():
            try:
                log.append(_normalize_raw_entry(_extract_raw_entry_fields(raw_log_line)))
            except (IndexError, ValueError):
                log.append(EMPTY_ENTRY)
    return log


def log_to_dict(log: list[Entry]) -> dict[str, list[EntryDict]]:
    result: dict[str, list[EntryDict]] = {}
    for entry in log:
        uid = entry.uid or "unknown"
        result.setdefault(uid, []).append(entry_to_dict(entry))
    return result


def entry_to_dict(entry: Entry) -> EntryDict:
    return {
        "ts": entry.ts,
        "uid": entry.uid,
        "orig_h": entry.orig_h,
        "orig_p": entry.orig_p,
        "resp_h": entry.resp_h,
        "resp_p": entry.resp_p,
        "method": entry.method,
        "host": entry.host,
        "uri": entry.uri,
        "status_code": entry.status_code,
        "size": entry.size,
        "date": entry.date,
        "time": entry.time,
        "timezone": entry.timezone,
    }
