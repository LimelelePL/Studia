import csv
from datetime import datetime
from pathlib import Path

from app.constants import (
    MEASUREMENTS_PATH,
    STATIONS_PATH,
    MeasurementsRawEntry,
    SingeMeasurement,
    StationData,
    StationEntry,
    StationSeries,
)


def parse_date(date_str: str) -> datetime | None:
    if not date_str or date_str.strip() == "":
        return None
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d")
    except ValueError:
        return None


def parse_measurement_datetime(date_str: str) -> datetime:
    value = date_str.strip()
    for date_format in ("%m/%d/%y %H:%M", "%d/%m/%y %H:%M"):
        try:
            return datetime.strptime(value, date_format)
        except ValueError:
            pass

    raise ValueError(f"Unsupported measurement datetime format: {date_str!r}")


def parse_stations() -> dict[str, list[StationData]]:
    result = {}

    with open(STATIONS_PATH, encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for entry in reader:
            code = entry[StationEntry.kod_stacji]

            result.setdefault(code, []).append(
                StationData(
                    nr=int(entry[StationEntry.nr]),
                    kod_stacji=code,
                    kod_miedzynarodowy=entry[StationEntry.kod_int] or None,
                    nazwa_stacji=entry[StationEntry.nazwa],
                    stary_kod_stacji=entry[StationEntry.stary_kod].strip() or None,
                    data_uruchomienia=parse_date(entry[StationEntry.data_uruchomienia]),
                    data_zamkniecia=parse_date(entry[StationEntry.data_zamkniecia]),
                    typ_stacji=entry[StationEntry.typ_stacji],
                    typ_obszaru=entry[StationEntry.typ_obszaru],
                    rodzaj_stacji=entry[StationEntry.rodzaj_stacji],
                    wojewodztwo=entry[StationEntry.wojewodztwo],
                    miejscowosc=entry[StationEntry.miejscowosc],
                    adres=entry[StationEntry.adres] or None,
                    wgs84_n=float(entry[StationEntry.WGS84_N].split()[0].replace(",", ".")),
                    wgs84_e=float(entry[StationEntry.WGS84_E].split()[0].replace(",", ".")),
                )
            )

    return result


def parse_measurment(file_name: Path) -> dict[str, list[StationSeries]]:
    path = MEASUREMENTS_PATH / file_name
    with open(path, encoding="utf-8") as file:
        rows = list(csv.reader(file))

        if not rows:
            return {}

    station_codes = rows[MeasurementsRawEntry.kod_stacji][1:]
    indicatiors = rows[MeasurementsRawEntry.wskaznik][1:]
    averaging_time = rows[MeasurementsRawEntry.czas_usrednienia][1:]
    unit = rows[MeasurementsRawEntry.jednostka][1:]
    code = rows[MeasurementsRawEntry.kod_stanowsika][1:]
    data_rows = rows[MeasurementsRawEntry.dane :]

    result = {}

    for idx, station_code in enumerate(station_codes, 1):
        series: list[SingeMeasurement] = []

        for row in data_rows:
            dt = parse_measurement_datetime(row[0])
            raw_val = row[idx].replace(",", ".") if idx < len(row) else ""
            val = float(raw_val) if raw_val.strip() else None
            series.append(SingeMeasurement(timestamp=dt, value=val))

        result.setdefault(station_code.strip(), []).append(
            StationSeries(
                kod_stacji=station_code.strip(),
                wskaznik=indicatiors[idx - 1].strip(),
                jednostka=unit[idx - 1].strip(),
                czas_usredniania=averaging_time[idx - 1].strip(),
                kod_stanowiska=code[idx - 1].strip(),
                pomiary=series,
            )
        )

    return result
