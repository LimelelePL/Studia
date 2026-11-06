import csv
import tempfile
from pathlib import Path

import pytest

from app.detectors import OutlierDetector, ThresholdDetector
from app.measurements import Measurements


def write_csv(path: Path, station_codes: list[str], sensor: str, avg: str, unit: str, rows: list[list[str]]) -> None:
    """Write a minimal measurement CSV with the expected header format."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        n_stations = len(station_codes)
        # Row 0: Nr
        writer.writerow(["Nr"] + [str(i + 1) for i in range(n_stations)])
        # Row 1: Kod stacji
        writer.writerow(["Kod stacji"] + station_codes)
        # Row 2: Wskaźnik
        writer.writerow(["Wskaźnik"] + [sensor] * n_stations)
        # Row 3: Czas uśredniania
        writer.writerow(["Czas uśredniania"] + [avg] * n_stations)
        # Row 4: Jednostka
        writer.writerow(["Jednostka"] + [unit] * n_stations)
        # Row 5: Kod stanowiska
        writer.writerow(["Kod stanowiska"] + [f"{c}-{sensor}-{avg}" for c in station_codes])
        # Data rows
        for row in rows:
            writer.writerow(row)


@pytest.fixture
def measurements_dir() -> Path:
    """Temporary directory with two CSV files."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        # File 1: C6H6, stations A and B
        write_csv(
            tmp_path / "2023_C6H6_1g.csv",
            station_codes=["StationA", "StationB"],
            sensor="C6H6",
            avg="1g",
            unit="ug/m3",
            rows=[
                ["01/01/23 01:00", "1.0", "5.0"],
                ["01/01/23 02:00", "2.0", "6.0"],
                ["01/01/23 03:00", "", "7.0"],  # missing value for A
            ],
        )

        # File 2: CO, station A only
        write_csv(
            tmp_path / "2023_CO_1g.csv",
            station_codes=["StationA"],
            sensor="CO",
            avg="1g",
            unit="mg/m3",
            rows=[
                ["01/01/23 01:00", "0.5"],
                ["01/01/23 02:00", "0.6"],
            ],
        )

        yield tmp_path


def test_len(measurements_dir: Path) -> None:
    m = Measurements(measurements_dir)
    # 2 stations in C6H6 file + 1 station in CO file = 3
    assert len(m) == 3


def test_contains_existing(measurements_dir: Path) -> None:
    m = Measurements(measurements_dir)
    assert "C6H6" in m
    assert "CO" in m


def test_contains_missing(measurements_dir: Path) -> None:
    m = Measurements(measurements_dir)
    assert "NO2" not in m


def test_get_by_parameter_c6h6(measurements_dir: Path) -> None:
    m = Measurements(measurements_dir)
    series_list = m.get_by_parameter("C6H6")
    assert len(series_list) == 2
    codes = {s.code for s in series_list}
    assert "StationA" in codes
    assert "StationB" in codes


def test_get_by_parameter_co(measurements_dir: Path) -> None:
    m = Measurements(measurements_dir)
    series_list = m.get_by_parameter("CO")
    assert len(series_list) == 1
    assert series_list[0].code == "StationA"


def test_get_by_parameter_nonexistent(measurements_dir: Path) -> None:
    m = Measurements(measurements_dir)
    assert m.get_by_parameter("NO2") == []


def test_get_by_station_a(measurements_dir: Path) -> None:
    m = Measurements(measurements_dir)
    series_list = m.get_by_station("StationA")
    # StationA has C6H6 and CO
    assert len(series_list) == 2
    sensors = {s.sensor for s in series_list}
    assert "C6H6" in sensors
    assert "CO" in sensors


def test_get_by_station_b(measurements_dir: Path) -> None:
    m = Measurements(measurements_dir)
    series_list = m.get_by_station("StationB")
    assert len(series_list) == 1
    assert series_list[0].sensor == "C6H6"


def test_get_by_station_nonexistent(measurements_dir: Path) -> None:
    m = Measurements(measurements_dir)
    assert m.get_by_station("Nonexistent") == []


def test_lazy_loading_no_cache_before_access(measurements_dir: Path) -> None:
    m = Measurements(measurements_dir)
    # No data should be loaded before any get_* call
    assert len(m._cache) == 0


def test_lazy_loading_partial_after_query(measurements_dir: Path) -> None:
    m = Measurements(measurements_dir)
    m.get_by_parameter("CO")
    # Only the CO file should have been loaded (1 series)
    assert len(m._cache) == 1


def test_detect_all_anomalies_preload_false(measurements_dir: Path) -> None:
    m = Measurements(measurements_dir)
    # Load only C6H6
    m.get_by_parameter("C6H6")
    result = m.detect_all_anomalies([ThresholdDetector(threshold=100.0)], preload=False)
    # Only 2 loaded series (C6H6 A and B), CO not yet loaded
    assert len(result) == 2


def test_detect_all_anomalies_preload_true(measurements_dir: Path) -> None:
    m = Measurements(measurements_dir)
    result = m.detect_all_anomalies([ThresholdDetector(threshold=100.0)], preload=True)
    # All 3 series loaded (C6H6 A, C6H6 B, CO A)
    assert len(result) == 3


def test_detect_all_anomalies_returns_dict(measurements_dir: Path) -> None:
    m = Measurements(measurements_dir)
    result = m.detect_all_anomalies([OutlierDetector(k=2.0)], preload=True)
    assert isinstance(result, dict)
    for val in result.values():
        assert isinstance(val, list)
