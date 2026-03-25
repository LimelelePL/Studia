from collections import Counter
from ipaddress import IPv4Address
from typing import cast

from app.constants import ENTRY_INDEXES_WITH_IP, EntryIndex
from app.my_types import Entry, EntryDict
from app.printing import get_num_of_requests


def get_top_ips(log: list[Entry], n: int = 10) -> list[tuple[IPv4Address, int]]:
    if n < 0:
        raise ValueError(f"Number of records can't be negative, given: {n}")
    ip_counts: Counter[IPv4Address] = Counter()
    for entry in log:
        for i in ENTRY_INDEXES_WITH_IP:
            if ip := cast(IPv4Address | None, entry[i]):
                ip_counts[ip] += 1

    return ip_counts.most_common(min(n, len(log)))


def count_status_classes(log: list[Entry]) -> dict[str, int]:
    status_code_counter: Counter[str] = Counter()
    for entry in log:
        if http_status := entry[EntryIndex.STATUS_CODE]:
            match http_status.value // 100:
                case 2:
                    status_code_counter["2xx"] += 1
                case 3:
                    status_code_counter["3xx"] += 1
                case 4:
                    status_code_counter["4xx"] += 1
                case 5:
                    status_code_counter["5xx"] += 1
                case _:
                    pass
    return dict(status_code_counter)


def count_by_method(log: list[Entry]) -> dict[str, int]:
    method_counter: Counter[str] = Counter()

    for entry in log:
        if method := entry[EntryIndex.METHOD]:
            method_counter[method] += 1

    return dict(method_counter)


def get_top_uris(log: list[Entry], n: int = 10) -> list[str]:
    if n < 0:
        raise ValueError(f"Number of records can't be negative, given: {n}")
    uris_counter: Counter[str] = Counter()

    for entry in log:
        if uri := entry[EntryIndex.URI]:
            uris_counter[uri] += 1
    most_common_uris = uris_counter.most_common(min(n, len(log)))

    return [uri for uri, _ in most_common_uris]


def session_with_most_request(log_dict: dict[str, list[EntryDict]]) -> str | None:
    max_num_of_requests = 0
    best_uid = None
    for uid, session in log_dict.items():
        num_of_requests = len(session)
        if num_of_requests > max_num_of_requests:
            max_num_of_requests = num_of_requests
            best_uid = uid
    return best_uid
