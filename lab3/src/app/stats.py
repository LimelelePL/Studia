from collections import Counter
from ipaddress import IPv4Address
from typing import cast

from app.constants import ENTRY_INDEXES_WITH_IP, EntryIndex
from app.my_types import Entry


def get_top_ips(log: list[Entry], n: int = 10) -> list[tuple[IPv4Address, int]]:
    if n < 0:
        raise ValueError(f"Number of records can't be negative, given: {n}")
    ip_counts: Counter[IPv4Address] = Counter()
    for entry in log:
        for i in ENTRY_INDEXES_WITH_IP:
            if ip := cast(IPv4Address | None, entry[i]):
                ip_counts[ip] += 1

    return ip_counts.most_common(min(n, len(log)))


def count_status_classes(log: list[Entry]) -> Counter[str]:
    stats_code_counter: Counter[str] = Counter()
    for entry in log:
        if http_status := entry[EntryIndex.STATUS_CODE]:
            match http_status.value // 100:
                case 2:
                    stats_code_counter["2xx"] += 1
                case 3:
                    stats_code_counter["3xx"] += 1
                case 4:
                    stats_code_counter["4xx"] += 1
                case 5:
                    stats_code_counter["5xx"] += 1
                case _:
                    pass
    return stats_code_counter
