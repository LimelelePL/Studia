import datetime
import sys
from typing import Any

from app.constants import EMPTY_FIELD
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
    except ValueError:
        return None


def _normalize_log_fields(log_fields: list[str]) -> HttpEntry:
    normalized = [None if x == EMPTY_FIELD else x for x in log_fields]
    ts, uid, orig_h, orig_p, resp_h, resp_p, method, host, uri = normalized  # tu moze być ValueError
    return (_to_datetime(ts), uid, orig_h, _to_int(orig_p), resp_h, _to_int(resp_p), method, host, uri)


def _retrive_log_fields(
    log_line: str,
) -> list[str]:
    fields = log_line.split()
    return [
        fields[0],
        fields[1],
        fields[2],
        fields[3],
        fields[4],
        fields[5],
        fields[7],
        fields[8],
        fields[9],
    ]


def read_log() -> list[HttpEntry]:
    logs: list[HttpEntry] = []
    for line in sys.stdin:
        if clean_line := line.strip():
            logs.append(_normalize_log_fields(_retrive_log_fields(clean_line)))
    return logs
