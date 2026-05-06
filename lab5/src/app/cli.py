import argparse
import logging
import random
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from statistics import mean, pstdev

from app.constants import MEASUREMENTS_PATH, STATIONS_PATH
from app.group_measurement_files_by_key import group_measurement_files_by_key
from app.parser import parse_measurment, parse_stations

logger = logging.getLogger(__name__)


@dataclass
class _MaxLevelFilter(logging.Filter):
    max_level: int

    def __post_init__(self) -> None:
        super().__init__()

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno < self.max_level


def setup_logging() -> None:
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    fmt = logging.Formatter("%(levelname)s %(name)s: %(message)s")

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.addFilter(_MaxLevelFilter(logging.ERROR))
    stdout_handler.setFormatter(fmt)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)
    stderr_handler.setFormatter(fmt)

    root.addHandler(stdout_handler)
    root.addHandler(stderr_handler)


def possible_unit_measurements(directory: Path) -> tuple[list[str], list[str]]:
    groupped_files = group_measurement_files_by_key(directory)
    measurements: set[str] = set()
    frequencies: set[str] = set()
    for _, measurement, frequency in groupped_files:
        measurements.add(measurement)
        frequencies.add(frequency)

    return (list(measurements), list(frequencies))


# bo w danych z pomiarami daty sa np. mm/dd/yy hh:mm
def convert_date(date: str) -> datetime:
    date = date.strip().split("\t")[0]
    formats = ("%m/%d/%y %H:%M", "%m/%d/%Y %H:%M", "%Y-%m-%d")

    for format_ in formats:
        try:
            return datetime.strptime(date, format_)
        except ValueError:
            continue

    raise ValueError(f"nieobslugiwany format daty: {date}")


def validate_date(date: str) -> datetime:
    try:
        return datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        msg = f"Nieprawidlowy format daty: '{date}'. Uzyj RRRR-MM-DD."
        raise argparse.ArgumentTypeError(msg)


def validate_date_range(parser: argparse.ArgumentParser, start: datetime, end: datetime) -> None:
    if start > end:
        parser.error("niepoprawny zakres dat")


def get_filtered_pathes(measurement: str, frequency: str) -> list[Path]:
    groupped_files = group_measurement_files_by_key(MEASUREMENTS_PATH)
    result: set[Path] = set()
    for (_, m, f), path in groupped_files.items():
        if m == measurement and f == frequency:
            result.add(path)

    if not result:
        logger.warning("Wskaźnik '%s' z częstotliwością '%s' nie występuje na żadnej stacji", measurement, frequency)

    return list(result)


def get_all_measurements_in_range(filtered_list: list[Path], start: datetime, end: datetime) -> list[dict]:
    result = []
    for file in filtered_list:
        data = parse_measurment(Path(file.name))
        for _, list_of_series in data.items():
            for series in list_of_series:
                for station_serie in series.pomiary:
                    timestamp = convert_date(station_serie.timestamp)

                    if start.date() <= timestamp.date() <= end.date():
                        record = {
                            "station_code": series.kod_stacji,
                            "value": station_serie.value,
                            "timestamp": timestamp,
                        }
                        result.append(record)

    if not result:
        logger.warning("Brak dostępnych pomiarów dla zadanych parametrów w podanym przedziale czasowym")

    return result


def get_name_and_address(station_code: str) -> dict[str, str]:
    stations = parse_stations(STATIONS_PATH)
    target = stations.get(station_code)

    if not target:
        logger.warning("Nie znaleziono stacji o kodzie: %s", station_code)
        return {}

    data = target[0]
    address = data.adres if data.adres else ""

    return {
        "station_name": data.nazwa_stacji,
        "station_city": data.miejscowosc,
        "station_address": address,
    }


def print_random_station(records: list[dict]) -> None:
    station_codes = list({record["station_code"] for record in records})

    if not station_codes:
        logger.warning("Brak stacji pomiarowych dla podanych parametrów")
        raise SystemExit(1)

    station_code = random.choice(station_codes)
    data = get_name_and_address(station_code)

    if not data:
        raise SystemExit(1)

    print(f"kod stacji: {station_code}")  # noqa: T201
    print(f"nazwa stacji: {data['station_name']}")  # noqa: T201
    print(f"miejscowosc: {data['station_city']}")  # noqa: T201
    print(f"adres: {data['station_address']}")  # noqa: T201


def print_stats(records: list[dict], station_code: str) -> None:
    values = [
        record["value"] for record in records if record["station_code"] == station_code and record["value"] is not None
    ]

    if not values:
        logger.warning(
            "Stacja '%s' nie wspiera podanego wskaźnika lub nie ma pomiarów w zadanym przedziale", station_code
        )
        raise SystemExit(1)

    print(f"kod stacji: {station_code}")  # noqa: T201
    print(f"liczba pomiarow: {len(values)}")  # noqa: T201
    print(f"srednia: {mean(values):.4f}")  # noqa: T201
    print(f"odchylenie standardowe: {pstdev(values):.4f}")  # noqa: T201


def parse_args():
    parser = argparse.ArgumentParser()
    measurements, frequencies = possible_unit_measurements(MEASUREMENTS_PATH)
    parser.add_argument("--sensor", required=True, choices=measurements, help="Mierzona wielkosc np PM10")
    parser.add_argument("--frequency", required=True, choices=frequencies, help="czestotliwosc pomiaru np 1g")
    parser.add_argument("--start", required=True, type=validate_date, help="poczatkowa data yyyy-mm-dd")
    parser.add_argument("--end", required=True, type=validate_date, help="koncowa data yyyy-mm-dd")

    subparsers = parser.add_subparsers(dest="command", required=True, help="dostepne akcje")
    subparsers.add_parser("random", help="Losowa stacja")
    parser_stats = subparsers.add_parser("stats", help="obliczenie statystyk dla danej stacji")
    parser_stats.add_argument("station_code", help="kod stacji")

    args = parser.parse_args()
    validate_date_range(parser, args.start, args.end)
    return args


def main() -> None:
    setup_logging()
    try:
        args = parse_args()
        filtered_list = get_filtered_pathes(args.sensor, args.frequency)

        if not filtered_list:
            raise SystemExit(1)

        records = get_all_measurements_in_range(filtered_list, args.start, args.end)

        if not records:
            raise SystemExit(1)

        if args.command == "random":
            print_random_station(records)

        elif args.command == "stats":
            print_stats(records, args.station_code)

    except FileNotFoundError:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
