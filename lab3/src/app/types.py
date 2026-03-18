import datetime

type HttpEntry = tuple[
    datetime.datetime | None,  # ts
    str | None,  # uid
    str | None,  # orig_h
    int | None,  # orig_p
    str | None,  # resp_h
    int | None,  # resp_p
    str | None,  # method
    str | None,  # host
    str | None,  # uri
]
