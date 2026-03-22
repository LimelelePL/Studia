from collections import Counter
from datetime import datetime
from http import HTTPStatus
from ipaddress import IPv4Address

from app.constants import EntryIndex
from app.converters import log_to_dict
from app.my_types import Entry, EntryDict


def get_paths(session: list[EntryDict]) -> list[str]:
    paths: list[str] = []
    for entry in session:
        if path := entry["uri"]:
            paths.append(path)
    return paths


# pytanie czy log w parametrze wedlug niego to lista logow,
# czy tez moze byc ten slownik
def get_session_paths(logs: list[Entry]) -> dict[str, list[str]]:

    logs_dict: dict[str, list[EntryDict]] = log_to_dict(logs)
    result: dict[str, list[str]] = {}
    for uid, session in logs_dict.items():
        result[uid] = get_paths(session)
    return result


# keku obczaj czy tak moze byc
def reqest_ratio_ipAddress(log: list[Entry], treshold: float) -> dict[IPv4Address, float]:
    request_count: Counter[IPv4Address] = Counter()
    for entry in log:
        if client_ip := entry[EntryIndex.ORIG_H]:
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


def is_error(status: HTTPStatus | None) -> bool:
    return status == HTTPStatus.NOT_FOUND


# liczy stosunek bledow 404 na liczbe zapytan z danego adresu ip
def ip_404_ratio(log: list[Entry], treshold_errors: float) -> dict[IPv4Address, float]:
    totals: Counter[IPv4Address] = Counter()
    not_found: Counter[IPv4Address] = Counter()

    for entry in log:
        if ip := entry[EntryIndex.ORIG_H]:
            totals[ip] += 1
            if is_error(entry[EntryIndex.STATUS_CODE]):
                not_found[ip] += 1

    result: dict[IPv4Address, float] = {}
    for ip in totals:
        if totals[ip]:
            ratio = not_found[ip] / totals[ip]
            if ratio > treshold_errors:
                result[ip] = not_found[ip] / totals[ip]
    return result


def count_short_intervals(log: list[Entry], threshold_miliseconds: float) -> dict[IPv4Address, float]:
    last_seen: dict[IPv4Address, datetime] = {}
    short_counts: Counter[IPv4Address] = Counter()
    total_pairs: Counter[IPv4Address] = Counter()

    for entry in log:
        if client_ip := entry[EntryIndex.ORIG_H]:
            if ts := entry[EntryIndex.TS]:
                if client_ip in last_seen:
                    if prev_ts := last_seen[client_ip]:
                        total_pairs[client_ip] += 1

                        if (ts - prev_ts).total_seconds() * 1000 < threshold_miliseconds:
                            short_counts[client_ip] += 1
                last_seen[client_ip] = ts

    result: dict[IPv4Address, float] = {}
    for ip, total in total_pairs.items():
        if total:
            result[ip] = short_counts[ip] / total
    return result


def detect_sus(
    log: list[Entry], req_treshold: float, err_treshold: float, interval_treshold_ms: float
) -> list[IPv4Address]:
    req_ratios: dict[IPv4Address, float] = reqest_ratio_ipAddress(log, req_treshold)
    err_ratios: dict[IPv4Address, float] = ip_404_ratio(log, err_treshold)
    interval_ratios: dict[IPv4Address, float] = count_short_intervals(log, interval_treshold_ms)

    suspects: set[IPv4Address] = set()

    suspects.update(req_ratios.keys())
    suspects.update(err_ratios.keys())
    suspects.update(interval_ratios.keys())

    return list(suspects)
