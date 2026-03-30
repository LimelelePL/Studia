from datetime import datetime
from ipaddress import IPv4Address

from app.my_types import Entry


def get_most_active_ip(log: list[Entry]) -> IPv4Address | None:
    last_seen: dict[IPv4Address, datetime] = {}
    total_pairs: dict[IPv4Address, float] = {}

    for entry in log:
        client_ip = entry.orig_h
        timestamp = entry.ts
        if not client_ip or not timestamp:
            continue

        prev_ts = last_seen.get(client_ip)
        if prev_ts:
            total_pairs[client_ip] = total_pairs.get(client_ip, 0.0) + (timestamp - prev_ts).total_seconds()

        last_seen[client_ip] = timestamp

    shortest = float("inf")
    min_addr: IPv4Address | None = None
    for k, v in total_pairs.items():
        if v < shortest:
            shortest = v
            min_addr = k

    return min_addr
