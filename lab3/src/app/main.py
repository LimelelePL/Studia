import sys

from printing import print_dict_entry_dates

from app.converters import log_to_dict, read_log
from app.my_types import Entry
from app.utils import format_stream_utf8

# TODO: change error messages to englishgi# TODO: napisać maila czy można uzywać HttpStatus i Ipv4Address z biblioteki standardowej
# TODO: Dodanie oblusgi bledow w przypadku podania niepoprawnego typu do funkcji
# TODO: na liscie nie ma wszystkich pol z ip w zadaniu 5
# Log- wszystkie dane, Entry - pojedynczy wpis, przedrostek RAW do niezformatowanych


def print_damaged_entries(log: list[Entry]) -> None:
    for entry in log:
        if entry.count(None):
            print(entry)


def print_log(log: list[Entry]) -> None:
    for entry in log:
        print(entry)


def print_log_field(log: list[Entry], ids: list[int]) -> None:
    for entry in log:
        print(tuple(entry[i] for i in ids))


def main() -> None:
    try:
        format_stream_utf8()
        log = read_log()
        log_dict = log_to_dict(log)
        # print_log(sort_log(log, EntryIndex.STATUS_CODE))
        # print_log(get_entries_by_code(log, HTTPStatus(400)))
        # print_log(get_entries_by_ip(log, IPv4Address("192.168.202.110")))
        # print_log(get_entries_by_ip(log, IPv4Address("999.999.999.999")))
        # client_errors, server_errors = get_failed_reads(log, False)
        # print_log(client_errors)
        # print_log(server_errors)
        # print_log(get_entries_by_extension(log, "php"))  # poprawne
        # print_log(get_entries_by_extension(log, ""))  # niepoprawne
        # print(*get_top_ips(log), sep="\n")
        # print(count_status_classes(log), sep="\n")
        # print(*get_unique_methods(log), sep="\n")
        # print(get_entries_in_time_range(log, datetime(1980, 3, 21, 19, 54), datetime(2026, 3, 21, 19, 54)), sep="\n")
        # print(count_by_method(log))
        # print(get_top_uris(log))
        print_dict_entry_dates(log_dict)

    except KeyboardInterrupt:
        sys.exit(0)  # użytkownik przerwał Ctrl+C
    except EOFError:
        sys.exit(0)  # stdin został zamknięty (np. koniec pliku)
    except BrokenPipeError:
        sys.exit(0)


if __name__ == "__main__":
    main()
