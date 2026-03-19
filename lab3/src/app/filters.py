from http import HTTPStatus

from app.constants import TUPLE_STATUS_CODE_INDEX
from app.types import HttpEntry
from app.constants import LOG_INDEXES_WITH_IP


def get_entries_by_code(logs: list[HttpEntry], code: int) -> list[HttpEntry]:
    try:
        _ = HTTPStatus(code)
    except ValueError as e:
        raise ValueError(
            f"Nie udało się zwrócić logów z odpowiednim kodem. Podano nieprawidłowy kod statusu HTTP: {code}"
        ) from e

    return [x for x in logs if x[TUPLE_STATUS_CODE_INDEX] == code]


def get_entries_by_ip(logs: list[HttpEntry], ip: str) -> list[HttpEntry]:
    return [x for x in logs if any(x[i] == ip for i in LOG_INDEXES_WITH_IP)]


# HACK : czy warto tutaj dodać obsluge nieprawidlowych statusow?
def get_failed_reads(
    logs: list[HttpEntry], merge: bool = False
) -> list[HttpEntry] | tuple[list[HttpEntry], list[HttpEntry]]:

    client_error_logs = [log for log in logs if 400 <= (log[TUPLE_STATUS_CODE_INDEX] or 0) <= 499]
    server_error_logs = [log for log in logs if 500 <= (log[TUPLE_STATUS_CODE_INDEX] or 0) <= 599]

    if merge:
        return client_error_logs + server_error_logs

    return client_error_logs, server_error_logs
