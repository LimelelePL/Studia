import datetime
import sys
from http import HTTPStatus
from ipaddress import IPv4Address
from typing import Any

from app.constants import EMPTY_ENTRY, EMPTY_FIELD, EntryIndex, RAW_LOG_FIELD_INDEXES
from app.types import Entry, EntryDict

# W przypadku braku pola lub jego uszkodzenia zamieniamy na None(uszkodzone mogą być pola: ts,orig_p,resp_p,
# reszta ewentualnie jest do dodania potem, bo jeszcze calej listy nie przeczytalem
# dobrze tez by bylo uzywac named tuple zamiast zwyklej ale trzeba napisac maila do tego cwela czy mozna


def _to_datetime(value: Any) -> datetime.datetime | None:
    # Obsługa błędu pojedynczego pola — uszkodzony timestamp zwraca None, reszta linii pozostaje niezmieniona
    try:
        return datetime.datetime.fromtimestamp(float(value))
    except (ValueError, OSError):
        return None


def _to_int(value: Any) -> int | None:
    # Obsługa błędu pojedynczego pola — uszkodzona liczba zwraca None, reszta linii pozostaje niezmieniona
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def _to_http_status(value: Any) -> HTTPStatus | None:
    # Obsługa błędu pojedynczego pola — niestandardowy lub uszkodzony kod zwraca None, reszta linii pozostaje niezmieniona
    try:
        return HTTPStatus(int(value))
    except (ValueError, TypeError):
        return None


def _to_ip(value: Any) -> IPv4Address | None:
    # Obsługa błędu pojedynczego pola — uszkodzony adres IP zwraca None, reszta linii pozostaje niezmieniona
    try:
        return IPv4Address(value)
    except (ValueError, TypeError):
        return None


def _normalize_raw_entry(raw_fields: list[str]) -> Entry:
    normalized = [None if x == EMPTY_FIELD else x for x in raw_fields]
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
        _to_http_status(status_code),
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
                # Obsługa błędu strukturalnego linii — zła liczba kolumn lub błąd rozpakowania,
                # cała linia jest uszkodzona i zastępowana pustą krotką
                log.append(EMPTY_ENTRY)
    return log


def log_to_dict(log: list[Entry]) -> dict[str, list[EntryDict]]:
    result: dict[str, list[EntryDict]] = {}
    for entry in log:
        uid = entry[EntryIndex.UID] or "unknown"
        result.setdefault(uid, []).append(entry_to_dict(entry))
    return result


def entry_to_dict(entry: Entry) -> EntryDict:
    return {
        "ts": entry[EntryIndex.TS],
        "uid": entry[EntryIndex.UID],
        "orig_h": entry[EntryIndex.ORIG_H],
        "orig_p": entry[EntryIndex.ORIG_P],
        "resp_h": entry[EntryIndex.RESP_H],
        "resp_p": entry[EntryIndex.RESP_P],
        "method": entry[EntryIndex.METHOD],
        "host": entry[EntryIndex.HOST],
        "uri": entry[EntryIndex.URI],
        "status_code": entry[EntryIndex.STATUS_CODE],
    }
