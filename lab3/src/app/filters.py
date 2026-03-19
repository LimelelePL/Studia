from http import HTTPStatus
from ipaddress import IPv4Address
from pathlib import Path
from typing import Literal, overload
from urllib.parse import urlparse

from app.constants import ENTRY_INDEXES_WITH_IP, EntryIndex
from app.types import Entry


# Trzeba sie zdecydować czy do funkcji podajemy int -> konwertujemy na HttpStatus, str i konwertujemy na ipv4 lub /
# podejmy httpStatus i ipv4 od razu, dwa podejscia (get_entries_by_code,get_entries_by_ip)


def get_entries_by_code(log: list[Entry], code: int) -> list[Entry]:
    try:
        status = HTTPStatus(code)
    except ValueError as e:
        raise ValueError(
            f"Nie udało się zwrócić logów z odpowiednim kodem. Podano nieprawidłowy kod statusu HTTP: {code}"
        ) from e

    return [x for x in log if x[EntryIndex.STATUS_CODE] == status]


def get_entries_by_ip(log: list[Entry], ip: IPv4Address) -> list[Entry]:
    return [x for x in log if any(x[i] == ip for i in ENTRY_INDEXES_WITH_IP)]


@overload
def get_failed_reads(log: list[Entry], merge: Literal[True]) -> list[Entry]: ...
@overload
def get_failed_reads(log: list[Entry], merge: Literal[False] = ...) -> tuple[list[Entry], list[Entry]]: ...


def get_failed_reads(log: list[Entry], merge: bool = False) -> list[Entry] | tuple[list[Entry], list[Entry]]:

    client_error_entries: list[Entry] = []
    server_error_entries: list[Entry] = []

    for entry in log:
        if s := entry[EntryIndex.STATUS_CODE]:
            if s.is_client_error:
                client_error_entries.append(entry)
            elif s.is_server_error:
                server_error_entries.append(entry)

    if merge:
        client_error_entries.extend(server_error_entries)
        return client_error_entries

    return (client_error_entries, server_error_entries)


def get_entries_by_extension(log: list[Entry], ext: str) -> list[Entry]:
    target_ext = f".{ext.lstrip('.')}"

    matched: list[Entry] = []
    for entry in log:
        if uri := entry[EntryIndex.URI]:
            path = urlparse(uri).path

            file_ext = Path(path).suffix

            if file_ext == target_ext:
                matched.append(entry)

    return matched
