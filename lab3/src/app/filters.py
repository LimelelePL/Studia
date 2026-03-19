from http import HTTPStatus
from ipaddress import IPv4Address
from pathlib import Path
from typing import Literal, overload
from urllib.parse import urlparse

from app.constants import LOG_INDEXES_WITH_IP, TUPLE_STATUS_CODE_INDEX, TUPLE_URI_INDEX
from app.types import HttpEntry


def get_entries_by_code(logs: list[HttpEntry], code: int) -> list[HttpEntry]:
    try:
        _ = HTTPStatus(code)
    except ValueError as e:
        raise ValueError(
            f"Nie udało się zwrócić logów z odpowiednim kodem. Podano nieprawidłowy kod statusu HTTP: {code}"
        ) from e

    return [x for x in logs if x[TUPLE_STATUS_CODE_INDEX] == code]


def get_entries_by_ip(logs: list[HttpEntry], ip: IPv4Address) -> list[HttpEntry]:
    return [x for x in logs if any(x[i] == ip for i in LOG_INDEXES_WITH_IP)]


@overload
def get_failed_reads(logs: list[HttpEntry], merge: Literal[True]) -> list[HttpEntry]: ...
@overload
def get_failed_reads(logs: list[HttpEntry], merge: Literal[False] = ...) -> tuple[list[HttpEntry], list[HttpEntry]]: ...
# HACK : czy warto tutaj dodać obsluge nieprawidlowych statusow?
def get_failed_reads(
    logs: list[HttpEntry], merge: bool = False
) -> list[HttpEntry] | tuple[list[HttpEntry], list[HttpEntry]]:

    client_error_logs: list[HttpEntry] = [log for log in logs if 400 <= (log[TUPLE_STATUS_CODE_INDEX] or 0) <= 499]
    server_error_logs: list[HttpEntry] = [log for log in logs if 500 <= (log[TUPLE_STATUS_CODE_INDEX] or 0) <= 599]

    if merge:
        return client_error_logs + server_error_logs

    return (client_error_logs, server_error_logs)


def get_entries_by_extension(logs: list[HttpEntry], ext: str) -> list[HttpEntry]:
    target_ext = f".{ext.lstrip('.')}"

    matched_logs: list[HttpEntry] = []
    for log in logs:
        if uri := log[TUPLE_URI_INDEX]:
            path = urlparse(uri).path

            file_ext = Path(path).suffix

            if file_ext == target_ext:
                matched_logs.append(log)

    return matched_logs
