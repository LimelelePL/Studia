import csv
from datetime import datetime
from pathlib import Path

import numpy as np

from app.constants import CSV_DATETIME_FORMAT, CsvHeaderField, CsvHeaderRow, SeriesEntry
from app.detectors import SeriesValidator
from app.timeseries import TimeSeries

_HEADER_ROWS_TO_READ = CsvHeaderRow.STATION_ID + 1   # read up to and including "Kod stanowiska"
_DATA_ROWS_START = CsvHeaderRow.STATION_ID + 1        # skip every header row before data


class Measurements:
    def __init__(self, directory: str | Path) -> None:
        self._directory = Path(directory)
        self._files: list[Path] = sorted(self._directory.glob("*.csv"))
        self._index: list[SeriesEntry] | None = None
        self._cache: dict[tuple[Path, str], TimeSeries] = {}
        self._loaded_files: set[Path] = set()

    def _ensure_index(self) -> None:
        """Read header rows from every CSV to build the index of available series."""
        if self._index is not None:
            return
        self._index = []
        for csv_file in self._files:
            with open(csv_file, encoding="utf-8", newline="") as f:
                reader = csv.reader(f)
                rows: list[list[str]] = []
                for _ in range(_HEADER_ROWS_TO_READ):
                    try:
                        rows.append(next(reader))
                    except StopIteration:
                        break
            if len(rows) < _HEADER_ROWS_TO_READ:
                continue
            station_codes = rows[CsvHeaderRow.STATION_CODE][CsvHeaderField.DATA_START:]
            sensors      = rows[CsvHeaderRow.SENSOR][CsvHeaderField.DATA_START:]
            avg_times    = rows[CsvHeaderRow.AVG_TIME][CsvHeaderField.DATA_START:]
            units        = rows[CsvHeaderRow.UNIT][CsvHeaderField.DATA_START:]
            for i, code in enumerate(station_codes):
                sensor = sensors[i]   if i < len(sensors)   else ""
                avg    = avg_times[i] if i < len(avg_times) else ""
                unit   = units[i]     if i < len(units)     else ""
                col_idx = i + CsvHeaderField.DATA_START
                self._index.append(SeriesEntry(csv_file, col_idx, code, sensor, avg, unit))

    def _load_file(self, file_path: Path) -> None:
        """Load all TimeSeries from a single CSV file and store them in the cache."""
        if file_path in self._loaded_files:
            return

        self._ensure_index()
        assert self._index is not None

        file_entries: list[SeriesEntry] = []
        for entry in self._index:
            if entry.file_path == file_path:
                file_entries.append(entry)

        rows_data: list[list[str]] = []
        with open(file_path, encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            for _ in range(_DATA_ROWS_START):
                next(reader, None)
            for row in reader:
                rows_data.append(row)

        for entry in file_entries:
            timestamps: list[datetime] = []
            raw_values: list[float | None] = []

            for row in rows_data:
                if not row or not row[CsvHeaderField.LABEL].strip():
                    continue
                try:
                    dt = datetime.strptime(row[CsvHeaderField.LABEL].strip(), CSV_DATETIME_FORMAT)
                except ValueError:
                    continue
                timestamps.append(dt)

                val_str = row[entry.col_idx].strip() if entry.col_idx < len(row) else ""
                try:
                    raw_values.append(float(val_str) if val_str else None)
                except ValueError:
                    raw_values.append(None)

            np_values = np.array([np.nan if v is None else v for v in raw_values], dtype=float)
            series = TimeSeries(
                sensor=entry.sensor,
                code=entry.station_code,
                averaging_time=entry.avg_time,
                timestamps=timestamps,
                values=np_values,
                unit=entry.unit,
            )
            self._cache[file_path, entry.station_code] = series

        self._loaded_files.add(file_path)

    def __len__(self) -> int:
        self._ensure_index()
        assert self._index is not None
        return len(self._index)

    def __contains__(self, parameter_name: object) -> bool:
        self._ensure_index()
        assert self._index is not None
        return any(entry.sensor == parameter_name for entry in self._index)

    def get_by_parameter(self, param_name: str) -> list[TimeSeries]:
        self._ensure_index()
        assert self._index is not None
        result: list[TimeSeries] = []
        seen: set[tuple[Path, str]] = set()
        for entry in self._index:
            if entry.sensor == param_name:
                self._load_file(entry.file_path)
                key = (entry.file_path, entry.station_code)
                if key in self._cache and key not in seen:
                    result.append(self._cache[key])
                    seen.add(key)
        return result

    def get_by_station(self, station_code: str) -> list[TimeSeries]:
        self._ensure_index()
        assert self._index is not None
        result: list[TimeSeries] = []
        seen: set[tuple[Path, str]] = set()
        for entry in self._index:
            if entry.station_code == station_code:
                self._load_file(entry.file_path)
                key = (entry.file_path, entry.station_code)
                if key in self._cache and key not in seen:
                    result.append(self._cache[key])
                    seen.add(key)
        return result

    def detect_all_anomalies(self, validators: list[SeriesValidator], preload: bool = False) -> dict[str, list[str]]:
        self._ensure_index()
        assert self._index is not None

        if preload:
            for entry in self._index:
                self._load_file(entry.file_path)

        result: dict[str, list[str]] = {}
        for series in self._cache.values():
            dict_key = f"{series.code}_{series.sensor}"
            messages: list[str] = []
            for validator in validators:
                messages.extend(validator.analyze(series))
            result[dict_key] = messages

        return result
