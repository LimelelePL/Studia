import csv
from datetime import datetime
from pathlib import Path

import numpy as np

from app.constants import CSV_DATETIME_FORMAT, CsvHeaderField, CsvHeaderRow, HEADER_ROW_COUNT, SeriesEntry
from app.detectors import SeriesValidator
from app.timeseries import TimeSeries


class Measurements:
    def __init__(self, directory: str | Path) -> None:
        self._directory = Path(directory)
        self._files: list[Path] = sorted(self._directory.glob("*.csv"))
        self._index: list[SeriesEntry] = []
        self._index_built = False
        self._cache: dict[tuple[Path, int], TimeSeries] = {}
        self._loaded_files: set[Path] = set()

    def _ensure_index(self) -> None:
        """Czyta wiersze nagłówka z każdego pliku CSV i buduje indeks dostępnych serii."""
        if self._index_built:
            return
        for csv_file in self._files:
            with open(csv_file, encoding="utf-8", newline="") as f:
                reader = csv.reader(f)
                rows: list[list[str]] = []
                for _ in range(HEADER_ROW_COUNT):
                    try:
                        rows.append(next(reader))
                    except StopIteration:
                        break
            if len(rows) < HEADER_ROW_COUNT:
                continue
            station_codes = rows[CsvHeaderRow.STATION_CODE][CsvHeaderField.DATA_START :]
            sensors = rows[CsvHeaderRow.SENSOR][CsvHeaderField.DATA_START :]
            avg_times = rows[CsvHeaderRow.AVG_TIME][CsvHeaderField.DATA_START :]
            units = rows[CsvHeaderRow.UNIT][CsvHeaderField.DATA_START :]
            for i, (code, sensor, avg, unit) in enumerate(zip(station_codes, sensors, avg_times, units, strict=False)):
                col_idx = i + CsvHeaderField.DATA_START
                self._index.append(SeriesEntry(csv_file, col_idx, code, sensor, avg, unit))
        self._index_built = True

    def _load_file(self, file_path: Path) -> None:
        """Wczytuje wszystkie serie czasowe z jednego pliku CSV i zapisuje je w cache."""
        if file_path in self._loaded_files:
            return

        self._ensure_index()

        file_entries: list[SeriesEntry] = []
        for entry in self._index:
            if entry.file_path == file_path:
                file_entries.append(entry)

        rows_data: list[list[str]] = []
        with open(file_path, encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            for _ in range(HEADER_ROW_COUNT):
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

            np_values = np.array(raw_values, dtype=float)
            series = TimeSeries(
                sensor=entry.sensor,
                code=entry.station_code,
                averaging_time=entry.avg_time,
                timestamps=timestamps,
                values=np_values,
                unit=entry.unit,
            )
            self._cache[file_path, entry.col_idx] = series

        self._loaded_files.add(file_path)

    def __len__(self) -> int:
        self._ensure_index()
        return len(self._index)

    def __contains__(self, parameter_name: object) -> bool:
        self._ensure_index()
        return any(entry.sensor == parameter_name for entry in self._index)

    def get_by_parameter(self, param_name: str) -> list[TimeSeries]:
        self._ensure_index()
        result: list[TimeSeries] = []
        for entry in self._index:
            if entry.sensor == param_name:
                self._load_file(entry.file_path)
                key = (entry.file_path, entry.col_idx)
                if key in self._cache:
                    result.append(self._cache[key])
        return result

    def get_by_station(self, station_code: str) -> list[TimeSeries]:
        self._ensure_index()
        result: list[TimeSeries] = []
        for entry in self._index:
            if entry.station_code == station_code:
                self._load_file(entry.file_path)
                key = (entry.file_path, entry.col_idx)
                if key in self._cache:
                    result.append(self._cache[key])
        return result

    def detect_all_anomalies(self, validators: list[SeriesValidator], preload: bool = False) -> dict[str, list[str]]:
        self._ensure_index()

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
