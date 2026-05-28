import datetime
import sys
from http import HTTPStatus
from ipaddress import IPv4Address
from typing import Any

from app.logs_parser.constants import EMPTY_ENTRY, EMPTY_FIELD, RAW_LOG_FIELD_INDEXES
from app.logs_parser.my_types import Entry, EntryDict

# W przypadku braku pola lub jego uszkodzenia zamieniamy na None(uszkodzone mogą być pola: ts,orig_p,resp_p,


def _to_datetime(value: Any) -> datetime.datetime | None:
    try:
        return datetime.datetime.fromtimestamp(float(value))
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
    ts, uid, orig_h, orig_p, resp_h, resp_p, method, host, uri, status_code = normalized_entry  # tu moze być ValueError
    return Entry(
        ts=_to_datetime(ts),
        uid=uid,
        orig_h=_to_ip(orig_h),
        orig_p=_to_int(orig_p),
        resp_h=_to_ip(resp_h),
        resp_p=_to_int(resp_p),
        method=method,
        host=_to_ip(host),
        uri=uri,
        status_code=_to_http_status(status_code),
    )


def _extract_raw_entry_fields(raw_log_line: str) -> list[str]:
    fields = raw_log_line.split("\t")
    # wybieramy tylko interesujące nas pola z tekstu
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


# klucz - uid, wartość lista slownikow (EntryDictKey - value)
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
    }
