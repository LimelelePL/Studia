import datetime
from collections import Counter
from ipaddress import IPv4Address

from app.logs_parser.constants import ENTRY_KEYS_WITH_IP, EntryDictKey
from app.logs_parser.my_types import Entry, EntryDict


def get_session_ips(session: list[EntryDict]) -> set[IPv4Address]:
    unique_hosts: set[IPv4Address] = set()
    for entry in session:
        for ip_key in ENTRY_KEYS_WITH_IP:
            if host := entry[ip_key]:
                unique_hosts.add(host)
    return unique_hosts


def get_first_request(session: list[EntryDict]) -> datetime.datetime | None:
    first = None
    for entry in session:
        if (ts := entry[EntryDictKey.TS]) and (first is None or ts < first):
            first = ts
    return first


def get_last_request(session: list[EntryDict]) -> datetime.datetime | None:
    last = None
    for entry in session:
        if (ts := entry[EntryDictKey.TS]) and (last is None or ts > last):
            last = ts
    return last


def get_propotion_of_methods(session: list[EntryDict]) -> dict[str, float]:
    method_counter: Counter[str] = Counter()

    for entry in session:
        if method := entry[EntryDictKey.METHOD]:
            method_counter[method] += 1

    total = sum(method_counter.values())
    if total == 0:
        return {}

    result: dict[str, float] = {}
    for method, count in method_counter.items():
        result[method] = count / total

    return result


def get_proportion_of_2xx_codes(session: list[EntryDict]) -> float:
    num_of_codes: int = 0
    num_of_2xx_codes: int = 0

    for entry in session:
        if code := entry[EntryDictKey.STATUS_CODE]:
            num_of_codes += 1
            if code.is_success:
                num_of_2xx_codes += 1

    return num_of_2xx_codes / num_of_codes if num_of_codes != 0 else 0.0


def print_dict_entry_dates(log_dict: dict[str, list[EntryDict]]) -> None:
    for uid, session in log_dict.items():
        print(f"=== SESJA ID: {uid} ===")
        print("adresy ip: ", get_session_ips(session))
        print("liczba żądań: ", len(session))
        print("pierwsze żądanie: ", get_first_request(session))
        print("ostatnie żądanie: ", get_last_request(session))
        print("procentowy udział metod http: ", get_propotion_of_methods(session))
        print("stosunek kodów 2xx do wszystkich: ", get_proportion_of_2xx_codes(session))
        print("-" * 30)
        print()


def print_damaged_entries(log: list[Entry]) -> None:
    for entry in log:
        if entry.count(None):
            print(entry)


def print_log(log: list[Entry]) -> None:
    for entry in log:
        print(entry)


def print_log_field(log: list[Entry], ids: list[int]) -> None:
    for entry in log:
        print(tuple(entry[i] for i in ids))
