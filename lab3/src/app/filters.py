from http import HTTPStatus
from ipaddress import IPv4Address
from pathlib import Path
from typing import Literal, overload
from urllib.parse import urlparse

from app.constants import ENTRY_INDEXES_WITH_IP, EntryIndex
from app.my_types import Entry


def get_entries_by_code(log: list[Entry], code: HTTPStatus) -> list[Entry]:
    return [x for x in log if x[EntryIndex.STATUS_CODE] == code]


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
        if status := entry[EntryIndex.STATUS_CODE]:
            if status.is_client_error:
                client_error_entries.append(entry)
            elif status.is_server_error:
                server_error_entries.append(entry)

    if merge:
        client_error_entries.extend(server_error_entries)
        return client_error_entries

    return (client_error_entries, server_error_entries)


def is_extension(ext: str) -> bool:
    clean_ext = ext.strip()
    return clean_ext.startswith(".") and len(clean_ext) > 1


def get_entries_by_extension(log: list[Entry], ext: str) -> list[Entry]:
    matched: list[Entry] = []
    if not is_extension(ext):
        raise ValueError("String have to be extension with '.'(dot) at beginning")
    target_ext = ext.lower()
    for entry in log:
        if uri := entry[EntryIndex.URI]:
            path = urlparse(uri).path

            file_ext = Path(path).suffix

            if file_ext == target_ext:
                matched.append(entry)

    return matched
