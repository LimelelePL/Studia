import datetime
from http import HTTPStatus
from ipaddress import IPv4Address
from pathlib import Path
from typing import Literal, overload
from urllib.parse import urlparse

from app.constants import ENTRY_INDEXES_WITH_IP
from app.my_types import Entry


def get_entries_by_code(log: list[Entry], code: HTTPStatus) -> list[Entry]:
    matched: list[Entry] = []
    for entry in log:
        if entry.status_code == code:
            matched.append(entry)
    return matched


def get_entries_by_ip(log: list[Entry], ip: IPv4Address) -> list[Entry]:
    matched: list[Entry] = []
    for entry in log:
        for i in ENTRY_INDEXES_WITH_IP:
            if entry[i] == ip:
                matched.append(entry)
                break
    return matched


@overload
def get_failed_reads(log: list[Entry], merge: Literal[True]) -> list[Entry]: ...
@overload
def get_failed_reads(log: list[Entry], merge: Literal[False] = ...) -> tuple[list[Entry], list[Entry]]: ...


def get_failed_reads(log: list[Entry], merge: bool = False) -> list[Entry] | tuple[list[Entry], list[Entry]]:

    client_error_entries: list[Entry] = []
    server_error_entries: list[Entry] = []

    for entry in log:
        if status := entry.status_code:
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
        if uri := entry.uri:
            path = urlparse(uri).path

            file_ext = Path(path).suffix

            if file_ext == target_ext:
                matched.append(entry)

    return matched


def get_unique_methods(log: list[Entry]) -> list[str]:
    unique_methods: set[str] = set()
    for entry in log:
        if method := entry.method:
            unique_methods.add(method)
    return list(unique_methods)


def is_in_date_range(start: datetime.datetime, end: datetime.datetime, target: datetime.datetime) -> bool:
    return start <= target < end


def get_entries_in_time_range(log: list[Entry], start: datetime.datetime, end: datetime.datetime) -> list[Entry]:
    entries_in_time_range: list[Entry] = []
    for entry in log:
        timestamp = entry.ts
        if timestamp and is_in_date_range(start, end, timestamp):
            entries_in_time_range.append(entry)
    return entries_in_time_range
