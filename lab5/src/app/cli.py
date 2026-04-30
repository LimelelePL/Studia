import argparse
import random
from datetime import datetime
from pathlib import Path
from statistics import mean, pstdev

from app.constants import MEASUREMENTS_PATH, STATIONS_PATH
from app.group_measurement_files_by_key import group_measurement_files_by_key
from app.parser import parse_measurment, parse_stations

SUPPORTED_FREQUENCIES = {"1g", "24g"}


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

    return result


def get_name_and_address(station_code: str) -> dict[str, str]:
    stations = parse_stations(STATIONS_PATH)
    target = stations.get(station_code)

    if not target:
        return {}

    data = target[0]
    address = data.adres if data.adres else ""

    return {
        "station_name": data.nazwa_stacji,
        "station_city": data.miejscowosc,
        "station_address": address,
    }


def print_random_station(records: list[dict]) -> None:
    station_codes = list(set(record["station_code"] for record in records))

    if not station_codes:
        raise SystemExit("brak stacji dla podanych parametrow")

    station_code = random.choice(station_codes)
    data = get_name_and_address(station_code)

    if not data:
        raise SystemExit(f"brak danych stacji: {station_code}")

    print(f"kod stacji: {station_code}")
    print(f"nazwa stacji: {data['station_name']}")
    print(f"miejscowosc: {data['station_city']}")
    print(f"adres: {data['station_address']}")


def print_stats(records: list[dict], station_code: str) -> None:
    values = [
        record["value"] for record in records if record["station_code"] == station_code and record["value"] is not None
    ]

    if not values:
        raise SystemExit("brak pomiarow dla podanej stacji i zakresu dat")

    print(f"kod stacji: {station_code}")
    print(f"liczba pomiarow: {len(values)}")
    print(f"srednia: {mean(values):.4f}")
    print(f"odchylenie standardowe: {pstdev(values):.4f}")


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
    args = parse_args()
    filtered_list = get_filtered_pathes(args.sensor, args.frequency)

    if not filtered_list:
        raise SystemExit("brak plikow dla podanych parametrow")

    records = get_all_measurements_in_range(filtered_list, args.start, args.end)

    if args.command == "random":
        print_random_station(records)
        return

    if args.command == "stats":
        print_stats(records, args.station_code)
        return


if __name__ == "__main__":
    main()
