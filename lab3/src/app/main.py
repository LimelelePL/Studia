import sys

from app.converters import read_log
from app.sorts import sort_log
from app.types import HttpEntry
from app.utils import format_stream_utf8
from app.filters import get_entries_by_code
# TODO: zmienic stale od indeksow bo w odnosza sie do pliku a nie krotki


def print_damaged_logs(logs: list[HttpEntry]) -> None:
    for log in logs:
        if log.count(None):
            print(log)


def print_all_logs(logs: list[HttpEntry]) -> None:
    for log in logs:
        print(log)


def print_logs_with_field(logs: list[HttpEntry], ids: list[int]) -> None:
    for log in logs:
        print(tuple(log[i] for i in ids))


def main() -> None:
    try:
        format_stream_utf8()
        logs = read_log()
        print_all_logs(sort_log(logs, 9))
        print_all_logs(get_entries_by_code(logs, 404))
    except KeyboardInterrupt:
        sys.exit(0)  # użytkownik przerwał Ctrl+C
    except EOFError:
        sys.exit(0)  # stdin został zamknięty (np. koniec pliku)
    except BrokenPipeError:
        sys.exit(0)


if __name__ == "__main__":
    main()
