from http import HTTPStatus
from ipaddress import IPv4Address

import pytest

from app.filters import get_entries_by_code, get_entries_by_extension, get_entries_by_ip, get_failed_reads
from app.my_types import Entry


def test_get_entries_by_code_returns_only_matching(log: list[Entry]) -> None:
    result = get_entries_by_code(log, 404)
    assert all(e[9] == HTTPStatus(404) for e in result)


def test_get_entries_by_code_invalid_raises(log: list[Entry]) -> None:
    with pytest.raises(ValueError):
        get_entries_by_code(log, 999)


def test_get_entries_by_code_nonempty(log: list[Entry]) -> None:
    result = get_entries_by_code(log, 404)
    assert len(result) > 0


def test_get_entries_by_ip_returns_only_matching(log: list[Entry]) -> None:
    ip = IPv4Address("192.168.202.79")
    result = get_entries_by_ip(log, ip)
    assert all(ip in (e[2], e[4], e[7]) for e in result)


def test_get_entries_by_ip_nonempty(log: list[Entry]) -> None:
    result = get_entries_by_ip(log, IPv4Address("192.168.202.79"))
    assert len(result) > 0


def test_get_failed_reads_split(log: list[Entry]) -> None:
    client_errors, server_errors = get_failed_reads(log)
    assert all(e[9] is not None and e[9].is_client_error for e in client_errors)
    assert all(e[9] is not None and e[9].is_server_error for e in server_errors)


def test_get_failed_reads_merge(log: list[Entry]) -> None:
    client_errors, server_errors = get_failed_reads(log)
    merged = get_failed_reads(log, merge=True)
    assert len(merged) == len(client_errors) + len(server_errors)


def test_get_entries_by_extension_nonempty(log: list[Entry]) -> None:
    result = get_entries_by_extension(log, ".php")
    assert len(result) > 0


def test_get_entries_by_extension_invalid_returns_empty(log: list[Entry]) -> None:
    result = get_entries_by_extension(log, "")
    assert result == []
