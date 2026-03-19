import sys
from ipaddress import IPv4Address

from app.constants import EntryIndex
from app.converters import read_log
from app.filters import get_entries_by_code, get_entries_by_extension, get_entries_by_ip, get_failed_reads
from app.sorts import sort_log
from app.types import Entry
from app.utils import format_stream_utf8

# TODO: change error messages to english
# TODO: napisać maila czy można uzywać HttpStatus i Ipv4Address z biblioteki standardowej
# TODO: Dodanie oblusgi bledow w przypadku podania niepoprawnego typu do funkcji
# TODO: na liscie nie ma wszystkich pol z ip w zadaniu 5


def print_damaged_entries(log: list[Entry]) -> None:
    for entry in log:
        if entry.count(None):
            print(entry)


def print_log(log: list[Entry]) -> None:
    for entry in log:
        print(entry)


def print_log_with_field(log: list[Entry], ids: list[int]) -> None:
    for entry in log:
        print(tuple(entry[i] for i in ids))


def main() -> None:
    try:
        format_stream_utf8()
        log = read_log()
        # print_log(sort_log(log, EntryIndex.STATUS_CODE))
        # print_log(get_entries_by_code(log, 404))
        print_log(get_entries_by_ip(log, IPv4Address("192.168.202.110")))
        # print_log(get_entries_by_ip(log, IPv4Address("999.999.999.999")))
        client_errors, server_errors = get_failed_reads(log, False)
        print_log(client_errors)
        # print_log(server_errors)
        # print_log(get_entries_by_extension(log, "php"))  # poprawne
        # print_log(get_entries_by_extension(log, ""))  # niepoprawne
    except KeyboardInterrupt:
        sys.exit(0)  # użytkownik przerwał Ctrl+C
    except EOFError:
        sys.exit(0)  # stdin został zamknięty (np. koniec pliku)
    except BrokenPipeError:
        sys.exit(0)


if __name__ == "__main__":
    main()
