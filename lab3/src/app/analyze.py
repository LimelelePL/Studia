from collections import Counter
from datetime import datetime
from http import HTTPStatus
from ipaddress import IPv4Address
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from app.constants import EntryDictKey, EntryIndex  # EntryIndex używany w sort_log
from app.converters import log_to_dict
from app.my_types import Entry, EntryDict
from app.sorts import sort_log
from app.stats import count_by_method, count_status_classes, get_top_ips, get_top_uris


def get_paths(session: list[EntryDict]) -> list[str]:
    paths: list[str] = []
    for entry in session:
        if path := entry[EntryDictKey.URI]:
            paths.append(path)
    return paths


def get_session_paths(logs: list[Entry]) -> dict[str, list[str]]:

    logs_dict: dict[str, list[EntryDict]] = log_to_dict(logs)
    result: dict[str, list[str]] = {}
    for uid, session in logs_dict.items():
        result[uid] = get_paths(session)
    return result


def request_ratio_ip(log: list[Entry], treshold: float) -> dict[IPv4Address, float]:
    request_count: Counter[IPv4Address] = Counter()
    for entry in log:
        if client_ip := entry.orig_h:
            request_count[client_ip] += 1

    total_requests = sum(request_count.values())
    if total_requests == 0:
        return {}

    result: dict[IPv4Address, float] = {}
    for ip, count in request_count.items():
        ratio = count / total_requests
        if ratio > treshold:
            result[ip] = count / total_requests
    return result


# liczy stosunek bledow 404 na liczbe zapytan z danego adresu ip
def ip_404_ratio(log: list[Entry], treshold_errors: float) -> dict[IPv4Address, float]:
    totals: Counter[IPv4Address] = Counter()
    not_found: Counter[IPv4Address] = Counter()

    for entry in log:
        if ip := entry.orig_h:
            totals[ip] += 1
            if entry.status_code == HTTPStatus.NOT_FOUND:
                not_found[ip] += 1

    result: dict[IPv4Address, float] = {}
    for ip in totals:
        ratio = not_found[ip] / totals[ip]
        if ratio > treshold_errors:
            result[ip] = ratio
    return result


# Oblicza dla każdego IP stosunek roznicy zapytan do wszystkich par zapytań tego adresu.
def count_short_intervals(log: list[Entry], threshold_miliseconds: float) -> dict[IPv4Address, float]:
    last_seen: dict[IPv4Address, datetime] = {}
    short_counts: Counter[IPv4Address] = Counter()
    total_pairs: Counter[IPv4Address] = Counter()

    for entry in log:
        client_ip = entry.orig_h
        timestamp = entry.ts
        if not client_ip or not timestamp:
            continue

        prev_ts = last_seen.get(client_ip)
        if prev_ts:
            total_pairs[client_ip] += 1
            if (timestamp - prev_ts).total_seconds() * 1000 < threshold_miliseconds:
                short_counts[client_ip] += 1

        last_seen[client_ip] = timestamp

    result: dict[IPv4Address, float] = {}
    for ip, total in total_pairs.items():
        if total:
            result[ip] = short_counts[ip] / total
    return result


def detect_sus(
    log: list[Entry], req_treshold: float, err_treshold: float, interval_treshold_ms: float
) -> list[IPv4Address]:
    req_ratios: dict[IPv4Address, float] = request_ratio_ip(log, req_treshold)
    err_ratios: dict[IPv4Address, float] = ip_404_ratio(log, err_treshold)
    interval_ratios: dict[IPv4Address, float] = count_short_intervals(log, interval_treshold_ms)

    suspects: set[IPv4Address] = set()

    suspects.update(req_ratios.keys())
    suspects.update(err_ratios.keys())
    suspects.update(interval_ratios.keys())

    return list(suspects)


def get_extension_stats(log: list[Entry]) -> dict[str, int]:
    extension_counter: Counter[str] = Counter()

    for entry in log:
        if uri := entry.uri:
            path = urlparse(uri).path
            file_ext = Path(path).suffix.lstrip(".").lower()
            if file_ext:
                extension_counter[file_ext] += 1

    return dict(extension_counter)


def calc_avg_interval(log: list[Entry]) -> float:
    sorted_by_ts: list[Entry] = sort_log(log, EntryIndex.TS)

    if not sorted_by_ts:
        return 0.0

    sum_of_times = 0.0
    no_of_times = 0
    for i in range(1, len(sorted_by_ts)):
        j = i - 1

        curr = sorted_by_ts[i].ts
        prev = sorted_by_ts[j].ts

        if not curr or not prev:
            continue

        diff = abs((prev - curr).total_seconds())
        sum_of_times += diff
        no_of_times += 1

    return 1000 * (sum_of_times / no_of_times) if no_of_times != 0 else 0.0


def analyze_log(log: list[Entry]) -> dict[str, Any]:
    top_ips: list[tuple[IPv4Address, int]] = get_top_ips(log, 3)
    top_uris: list[str] = get_top_uris(log, 3)
    method_distribution: dict[str, int] = count_by_method(log)
    status_classes_count = count_status_classes(log)
    error_count: int = status_classes_count["4xx"] + status_classes_count["5xx"]
    no_of_uid: int = len(log_to_dict(log))
    avg_interval_ms = calc_avg_interval(log)

    return {
        "top_ips": top_ips,
        "top_uris": top_uris,
        "error_count": error_count,
        "no_of_uid": no_of_uid,
        "avg_interval_ms": avg_interval_ms,
        "method_distribution": method_distribution,
    }
