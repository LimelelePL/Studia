import datetime
from http import HTTPStatus
from ipaddress import IPv4Address

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
