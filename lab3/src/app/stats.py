from collections import Counter
from ipaddress import IPv4Address
from typing import cast

from app.constants import ENTRY_INDEXES_WITH_IP
from app.types import Entry


def get_top_ips(log: list[Entry], n: int = 10) -> list[tuple[IPv4Address, int]]:
    if n < 0:
        raise ValueError(f"Number of records can't be negative, given: {n}")
    ip_counts: Counter[IPv4Address] = Counter()

    for entry in log:
        for i in ENTRY_INDEXES_WITH_IP:
            if ip := cast(IPv4Address | None, entry[i]):
                ip_counts[ip] += 1

    return ip_counts.most_common(n)
