import datetime
import sys
from ipaddress import IPv4Address
from typing import Any

from app.constants import (
    EMPTY_FIELD,
    LOG_HOST_INDEX,
    LOG_METHOD_INDEX,
    LOG_ORIG_H_INDEX,
    LOG_ORIG_P_INDEX,
    LOG_RESP_H_INDEX,
    LOG_RESP_P_INDEX,
    LOG_STATUS_CODE_INDEX,
    LOG_TS_INDEX,
    LOG_UID_INDEX,
    LOG_URI_INDEX,
)
from app.types import HttpEntry

# W przypadku braku pola lub jego uszkodzenia zamieniamy na None(uszkodzone mogą być pola: ts,orig_p,resp_p,
# reszta ewentualnie jest do dodania potem, bo jeszcze calej listy nie przeczytalem
# dobrze tez by bylo uzywac named tuple zamiast zwyklej ale trzeba napisac maila do tego cwela czy mozna


def _to_datetime(value: Any) -> datetime.datetime | None:
    try:
        return datetime.datetime.fromtimestamp(float(value))
    except (ValueError, OSError):
        return None


def _to_int(value: Any) -> int | None:
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def _to_ip(value: Any) -> IPv4Address | None:
    try:
        return IPv4Address(value)
    except (ValueError, TypeError):
        return None


def _normalize_log_fields(log_fields: list[str]) -> HttpEntry:
    normalized = [None if x == EMPTY_FIELD else x for x in log_fields]
    ts, uid, orig_h, orig_p, resp_h, resp_p, method, host, uri, status_code = normalized  # tu moze być ValueError
    return (
        _to_datetime(ts),
        uid,
        _to_ip(orig_h),
        _to_int(orig_p),
        _to_ip(resp_h),
        _to_int(resp_p),
        method,
        _to_ip(host),
        uri,
        _to_int(status_code),
    )


def _retrive_log_fields(
    log_line: str,
) -> list[str]:
    fields = log_line.split("\t")
    return [
        fields[LOG_TS_INDEX],
        fields[LOG_UID_INDEX],
        fields[LOG_ORIG_H_INDEX],
        fields[LOG_ORIG_P_INDEX],
        fields[LOG_RESP_H_INDEX],
        fields[LOG_RESP_P_INDEX],
        fields[LOG_METHOD_INDEX],
        fields[LOG_HOST_INDEX],
        fields[LOG_URI_INDEX],
        fields[LOG_STATUS_CODE_INDEX],
    ]


def read_log() -> list[HttpEntry]:
    logs: list[HttpEntry] = []
    for line in sys.stdin:
        if clean_line := line.strip():
            logs.append(_normalize_log_fields(_retrive_log_fields(clean_line)))
    return logs
