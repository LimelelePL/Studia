from ipaddress import IPv4Address
from http import HTTPStatus
import datetime

from app.converters import entry_to_dict, log_to_dict
from app.types import Entry


def test_entry_to_dict_keys(log: list[Entry]) -> None:
    d = entry_to_dict(log[0])
    assert set(d.keys()) == {"ts", "uid", "orig_h", "orig_p", "resp_h", "resp_p", "method", "host", "uri", "status_code"}


def test_entry_to_dict_types(log: list[Entry]) -> None:
    for entry in log[:100]:
        d = entry_to_dict(entry)
        assert d["ts"] is None or isinstance(d["ts"], datetime.datetime)
        assert d["uid"] is None or isinstance(d["uid"], str)
        assert d["orig_h"] is None or isinstance(d["orig_h"], IPv4Address)
        assert d["orig_p"] is None or isinstance(d["orig_p"], int)
        assert d["status_code"] is None or isinstance(d["status_code"], HTTPStatus)


def test_log_to_dict_all_entries_present(log: list[Entry]) -> None:
    grouped = log_to_dict(log)
    total = sum(len(entries) for entries in grouped.values())
    assert total == len(log)


def test_log_to_dict_grouped_by_uid(log: list[Entry]) -> None:
    grouped = log_to_dict(log)
    for uid, entries in grouped.items():
        assert all(e[1] == uid for e in entries)


def test_log_to_dict_none_key_for_damaged(log: list[Entry]) -> None:
    grouped = log_to_dict(log)
    if None in grouped:
        assert all(e[1] is None for e in grouped[None])
