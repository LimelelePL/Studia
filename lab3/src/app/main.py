import sys

from app.analyze import get_most_active_ip
from app.converters import read_log
from app.utils import format_stream_utf8


def main() -> None:
    try:
        format_stream_utf8()
        log = read_log()
        # log_dict = log_to_dict(log)
        # print_log_field(sort_log(log, EntryIndex.STATUS_CODE), [EntryIndex.STATUS_CODE])
        # print_log_field(get_entries_by_code(log, HTTPStatus(400)), [EntryIndex.STATUS_CODE])
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
        # print(get_entries_in_ti
        # me_range(log, datetime(1980, 3, 21, 19, 54), datetime(2026, 3, 21, 19, 54)), sep="\n")
        # print(count_by_method(log))
        # print(get_top_uris(log))
        # print_dict_entry_dates(log_dict)
        # print(session_with_most_request(log_dict))
        # print(get_session_paths(log))
        print(get_most_active_ip(log))
        # print(detect_sus(log, 0.02, 0.15, 50))
        # print(get_extension_stats(log))
        # print(analyze_log(log))

        # print(log_dict, sep="\n")

    except KeyboardInterrupt:
        sys.exit(0)
    except EOFError:
        sys.exit(0)
    except BrokenPipeError:
        sys.exit(0)
    except OSError as e:
        print(f"Błąd odczytu z wejścia standardwoego: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
