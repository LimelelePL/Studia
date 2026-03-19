import datetime
from ipaddress import IPv4Address

type HttpEntry = tuple[
    datetime.datetime | None,  # ts
    str | None,  # uid
    IPv4Address | None,  # orig_h
    int | None,  # orig_p
    IPv4Address | None,  # resp_h
    int | None,  # resp_p
    str | None,  # method
    IPv4Address | None,  # host
    str | None,  # uri
    int | None,  # status_code
]
# orig_h, resp_h,host
