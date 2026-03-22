"""
Napisz funkcję print_dict_entry_dates(log_dict), która dla każdej sesji:
-  wypisuje:  adresy IP / hosty, liczbę żądań, datę pierwszego i ostatniego żądania.
-  procentowy udział metod HTTP
-  stosunek liczby kodów 2xx do wszystkich
"""

import datetime
from collections import Counter
from ipaddress import IPv4Address

from app.my_types import EntryDict


def get_session_hosts(session: list[EntryDict]) -> list[IPv4Address]:
    unique_hosts: set[IPv4Address] = set()
    for entry in session:
        if host := entry["host"]:
            unique_hosts.add(host)
    return list(unique_hosts)


def get_num_of_requests(session: list[EntryDict]) -> int:
    return len(session)


def get_first_request(session: list[EntryDict]) -> datetime.datetime | None:
    first: datetime.datetime | None = None
    for entry in session:
        if ts := entry["ts"]:
            if first is None or ts < first:
                first = ts
    return first


def get_last_request(session: list[EntryDict]) -> datetime.datetime | None:
    last: datetime.datetime | None = None
    for entry in session:
        if ts := entry["ts"]:
            if last is None or ts > last:
                last = ts
    return last


def get_propotion_of_methods(session: list[EntryDict]) -> dict[str, float]:
    count_method_freq: Counter[str] = Counter()

    for entry in session:
        if method := entry["method"]:
            count_method_freq[method] += 1

    total = sum(count_method_freq.values())
    if total == 0:
        return {}

    result: dict[str, float] = {}
    for method, count in count_method_freq.items():
        result[method] = count / total

    return result


def get_proportion_of_2xx_codes(session: list[EntryDict]) -> float:
    num_of_codes: int = 0
    num_of_2xx_codes: int = 0

    for entry in session:
        if code := entry["status_code"]:
            num_of_codes += 1
            if code.value // 100 == 2:
                num_of_2xx_codes += 1

    return num_of_2xx_codes / num_of_codes if num_of_codes != 0 else 0.0


def print_dict_entry_dates(log_dict: dict[str, list[EntryDict]]) -> None:
    for uid, session in log_dict.items():
        print(f"=== SESJA ID: {uid} ===")
        print("hosty: ", get_session_hosts(session))
        print("liczba żądań: ", get_num_of_requests(session))
        print("pierwsze żądanie: ", get_first_request(session))
        print("ostatnie żądanie: ", get_last_request(session))
        print("procentowy udział metod http: ", get_propotion_of_methods(session))
        print("stosunek kodów 2xx do wszystkich: ", get_proportion_of_2xx_codes(session))
        print("-" * 30)
        print()
