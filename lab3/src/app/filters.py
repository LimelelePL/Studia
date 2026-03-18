from http import HTTPStatus
from ipaddress import IPv4Address

from app.constants import TUPLE_HOST_INDEX, TUPLE_ORIG_H_INDEX, TUPLE_RESP_H_INDEX, TUPLE_STATUS_CODE_INDEX
from app.types import HttpEntry


def get_entries_by_code(logs: list[HttpEntry], code: int) -> list[HttpEntry]:
    try:
        _ = HTTPStatus(code)
    except ValueError as e:
        raise ValueError(
            f"Nie udało się zwrócić logów z odpowiednim kodem. Podano nieprawidłowy kod statusu HTTP: {code}"
        ) from e

    return [x for x in logs if x[TUPLE_STATUS_CODE_INDEX] == code]


def get_entries_by_ip(logs: list[HttpEntry], ip: IPv4Address) -> list[HttpEntry]:
    return [x for x in logs if x[TUPLE_ORIG_H_INDEX] == ip or x[TUPLE_RESP_H_INDEX] == ip or x[TUPLE_HOST_INDEX] == ip]
