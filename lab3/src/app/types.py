import datetime
from http import HTTPStatus
from ipaddress import IPv4Address
from typing import TypedDict

type Entry = tuple[
    datetime.datetime | None,  # ts
    str | None,  # uid
    IPv4Address | None,  # orig_h
    int | None,  # orig_p
    IPv4Address | None,  # resp_h
    int | None,  # resp_p
    str | None,  # method
    IPv4Address | None,  # host
    str | None,  # uri
    HTTPStatus | None,  # status_code
]
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
