import datetime
from http import HTTPStatus
from ipaddress import IPv4Address
from typing import NamedTuple, TypedDict


class Entry(NamedTuple):
    ts: datetime.datetime | None
    uid: str | None
    orig_h: IPv4Address | None
    orig_p: int | None
    resp_h: IPv4Address | None
    resp_p: int | None
    method: str | None
    host: IPv4Address | None
    uri: str | None
    status_code: HTTPStatus | None
    size: int | None
    date: datetime.date | None
    time: datetime.time | None
    timezone: str | None


type Extension = str


class EntryDict(TypedDict):
    ts: datetime.datetime | None
    uid: str | None
    orig_h: IPv4Address | None
    orig_p: int | None
    resp_h: IPv4Address | None
    resp_p: int | None
    method: str | None
    host: IPv4Address | None
    uri: str | None
    status_code: HTTPStatus | None
    size: int | None
    date: datetime.date | None
    time: datetime.time | None
    timezone: str | None
