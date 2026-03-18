import sys

from ipaddress import IPv4Address

from app.constants import TUPLE_STATUS_CODE_INDEX
from app.converters import read_log
from app.filters import get_entries_by_code, get_entries_by_ip
from app.sorts import sort_log
from app.types import HttpEntry
from app.utils import format_stream_utf8
# TODO: change error messages to english
# TODO: napisać maila czy można uzywać HttpStatus i Ipv4Address z biblioteki standardowej
# TODO: Dodanie oblusgi bledow w przypadku podania niepoprawnego typu do funkcji


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
        # print_all_logs(sort_log(logs, TUPLE_STATUS_CODE_INDEX))
        # print_all_logs(get_entries_by_code(logs, 404))
        print_all_logs(get_entries_by_ip(logs, IPv4Address("192.168.202.110")))
        print_all_logs(get_entries_by_ip(logs, IPv4Address("999.999.999.999")))
    except KeyboardInterrupt:
        sys.exit(0)  # użytkownik przerwał Ctrl+C
    except EOFError:
        sys.exit(0)  # stdin został zamknięty (np. koniec pliku)
    except BrokenPipeError:
        sys.exit(0)


if __name__ == "__main__":
    main()
