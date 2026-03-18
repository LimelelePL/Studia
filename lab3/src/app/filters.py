from http import HTTPStatus

from app.types import HttpEntry


def get_entries_by_code(logs: list[HttpEntry], code: int) -> list[HttpEntry]:
    try:
        _ = HTTPStatus(code)
    except ValueError as e:
        raise ValueError(
            f"Nie udało się zwrócić logów z odpowiednim kodem. Podano nieprawidłowy kod statusu HTTP: {code}"
        ) from e

    return [x for x in logs if x[9] == code]
