from enum import IntEnum
from pathlib import Path
from typing import NamedTuple


class CsvHeaderRow(IntEnum):
    """Row index of each metadata line in the CSV header block."""

    STATION_CODE = 1
    SENSOR = 2
    AVG_TIME = 3
    UNIT = 4
    STATION_ID = 5  # "Kod stanowiska" — ostatni nagłówek przed danymi


HEADER_ROW_COUNT = CsvHeaderRow.STATION_ID + 1  # liczba wierszy nagłówka przed danymi


class CsvHeaderField(IntEnum):
    """Column index of the label field in every header / data row."""

    LABEL = 0  # "Kod stacji"
    DATA_START = 1


CSV_DATETIME_FORMAT = "%d/%m/%y %H:%M"


class SeriesEntry(NamedTuple):
    """One entry in the Measurements index — describes a single loadable TimeSeries."""

    file_path: Path
    col_idx: int
    station_code: str
    sensor: str
    avg_time: str
    unit: str
