import csv
import logging
from pathlib import Path

from app.constants import (
    MEASUREMENTS_PATH,
    MeasurementsRawEntry,
    SingeMeasurement,
    StationData,
    StationEntry,
    StationSeries,
)

# dane typu data szerokosc geograficzna sa stringami bo trzeba pozniej w zadaniach operowac na nich regexem

logger = logging.getLogger(__name__)


def parse_stations(path: Path) -> dict[str, list[StationData]]:
    result = {}

    if not path.is_file():
        logger.error("Plik nie istnieje: %s", path)
        raise FileNotFoundError(f"Plik nie istnieje: {path}")

    logger.info("Otwarto plik: %s", path)
    with open(path, encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for entry in reader:
            logger.debug("Przeczytano %d bajtow", len(",".join(entry.values()).encode("utf-8")))
            code = entry[StationEntry.kod_stacji]

            result.setdefault(code, []).append(
                StationData(
                    nr=int(entry[StationEntry.nr]),
                    kod_stacji=code,
                    kod_miedzynarodowy=entry[StationEntry.kod_int] or None,
                    nazwa_stacji=entry[StationEntry.nazwa],
                    stary_kod_stacji=entry[StationEntry.stary_kod].strip() or None,
                    data_uruchomienia=entry[StationEntry.data_uruchomienia].strip(),
                    data_zamkniecia=entry[StationEntry.data_zamkniecia].strip(),
                    typ_stacji=entry[StationEntry.typ_stacji],
                    typ_obszaru=entry[StationEntry.typ_obszaru],
                    rodzaj_stacji=entry[StationEntry.rodzaj_stacji],
                    wojewodztwo=entry[StationEntry.wojewodztwo],
                    miejscowosc=entry[StationEntry.miejscowosc],
                    adres=entry[StationEntry.adres] or None,
                    wgs84_n=entry[StationEntry.WGS84_N].split()[0].replace(",", "."),
                    wgs84_e=entry[StationEntry.WGS84_E].split()[0].replace(",", "."),
                )
            )
    logger.info("Zamknieto plik: %s", path)

    return result


def parse_measurment(file_name: Path) -> dict[str, list[StationSeries]]:
    path = MEASUREMENTS_PATH / file_name

    if not path.is_file():
        logger.error("Plik nie istnieje: %s", path)
        raise FileNotFoundError(f"Plik nie istnieje: {path}")

    logger.info("Otwarto plik: %s", path)
    with open(path, encoding="utf-8") as file:
        rows = list(csv.reader(file))
    logger.info("Zamknieto plik: %s", path)

    if not rows:
        return {}

    station_codes = rows[MeasurementsRawEntry.kod_stacji][1:]
    indicators = rows[MeasurementsRawEntry.wskaznik][1:]
    averaging_time = rows[MeasurementsRawEntry.czas_usrednienia][1:]
    unit = rows[MeasurementsRawEntry.jednostka][1:]
    code = rows[MeasurementsRawEntry.kod_stanowiska][1:]
    data_rows = rows[MeasurementsRawEntry.dane :]

    for row in data_rows:
        logger.debug("Przeczytano %d bajtow", len(",".join(row).encode("utf-8")))

    result = {}

    for idx, station_code in enumerate(station_codes, 1):
        series: list[SingeMeasurement] = []

        for row in data_rows:
            dt = row[0]
            raw_val = row[idx].replace(",", ".") if idx < len(row) else ""
            val = float(raw_val) if raw_val.strip() else None
            series.append(SingeMeasurement(timestamp=dt, value=val))

        result.setdefault(station_code.strip(), []).append(
            StationSeries(
                kod_stacji=station_code.strip(),
                wskaznik=indicators[idx - 1].strip(),
                jednostka=unit[idx - 1].strip(),
                czas_usredniania=averaging_time[idx - 1].strip(),
                kod_stanowiska=code[idx - 1].strip(),
                pomiary=series,
            )
        )

    return result
