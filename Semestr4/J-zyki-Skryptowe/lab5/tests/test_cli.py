import argparse
import logging
import pytest
from datetime import datetime
from pathlib import Path

from app.cli import (
    _MaxLevelFilter,
    convert_date,
    get_all_measurements_in_range,
    get_filtered_pathes,
    validate_date,
    validate_date_range,
)


# --- _MaxLevelFilter ---

def test_max_level_filter_passes_below_threshold():
    f = _MaxLevelFilter(logging.ERROR)
    record = logging.LogRecord("test", logging.WARNING, "", 0, "msg", (), None)
    assert f.filter(record) is True


def test_max_level_filter_blocks_at_threshold():
    f = _MaxLevelFilter(logging.ERROR)
    record = logging.LogRecord("test", logging.ERROR, "", 0, "msg", (), None)
    assert f.filter(record) is False


def test_max_level_filter_blocks_above_threshold():
    f = _MaxLevelFilter(logging.ERROR)
    record = logging.LogRecord("test", logging.CRITICAL, "", 0, "msg", (), None)
    assert f.filter(record) is False


# --- convert_date ---

@pytest.mark.parametrize("date_str,expected", [
    ("01/01/23 01:00", datetime(2023, 1, 1, 1, 0)),
    ("12/31/2023 23:59", datetime(2023, 12, 31, 23, 59)),
    ("2023-01-15", datetime(2023, 1, 15)),
])
def test_convert_date(date_str, expected):
    assert convert_date(date_str) == expected


def test_convert_date_invalid_raises():
    with pytest.raises(ValueError, match="nieobslugiwany format daty"):
        convert_date("not-a-date")


# --- validate_date ---

def test_validate_date_returns_datetime():
    assert validate_date("2023-06-15") == datetime(2023, 6, 15)


def test_validate_date_invalid_format_raises():
    with pytest.raises(argparse.ArgumentTypeError):
        validate_date("15-06-2023")


def test_validate_date_non_date_raises():
    with pytest.raises(argparse.ArgumentTypeError):
        validate_date("not-a-date")


# --- validate_date_range ---

def test_validate_date_range_valid_does_not_raise():
    parser = argparse.ArgumentParser()
    validate_date_range(parser, datetime(2023, 1, 1), datetime(2023, 12, 31))


def test_validate_date_range_same_day_does_not_raise():
    parser = argparse.ArgumentParser()
    validate_date_range(parser, datetime(2023, 6, 1), datetime(2023, 6, 1))


def test_validate_date_range_reversed_raises():
    parser = argparse.ArgumentParser()
    with pytest.raises(SystemExit):
        validate_date_range(parser, datetime(2023, 12, 31), datetime(2023, 1, 1))


# --- get_filtered_pathes (integration) ---

def test_get_filtered_pathes_returns_paths_for_existing_measurement():
    result = get_filtered_pathes("PM10", "1g")
    assert len(result) > 0
    assert all(isinstance(p, Path) for p in result)


def test_get_filtered_pathes_warns_for_nonexistent_measurement(caplog):
    with caplog.at_level(logging.WARNING, logger="app.cli"):
        result = get_filtered_pathes("NONEXISTENT", "1g")
    assert result == []
    assert any("nie występuje na żadnej stacji" in r.message for r in caplog.records)


# --- get_all_measurements_in_range ---

def test_get_all_measurements_in_range_returns_records_in_date_range(measurements_dir, monkeypatch):
    monkeypatch.setattr("app.parser.MEASUREMENTS_PATH", measurements_dir)
    paths = [measurements_dir / "2023_PM10_1g.csv"]
    start = datetime(2023, 1, 1)
    end = datetime(2023, 1, 1)

    result = get_all_measurements_in_range(paths, start, end)

    assert len(result) > 0
    assert all(r["timestamp"].date() == start.date() for r in result)


def test_get_all_measurements_in_range_excludes_out_of_range(measurements_dir, monkeypatch):
    monkeypatch.setattr("app.parser.MEASUREMENTS_PATH", measurements_dir)
    paths = [measurements_dir / "2023_PM10_1g.csv"]

    result = get_all_measurements_in_range(paths, datetime(2020, 1, 1), datetime(2020, 12, 31))

    assert result == []


def test_get_all_measurements_in_range_warns_when_empty(measurements_dir, monkeypatch, caplog):
    monkeypatch.setattr("app.parser.MEASUREMENTS_PATH", measurements_dir)
    paths = [measurements_dir / "2023_PM10_1g.csv"]

    with caplog.at_level(logging.WARNING, logger="app.cli"):
        result = get_all_measurements_in_range(paths, datetime(2020, 1, 1), datetime(2020, 1, 31))

    assert result == []
    assert any("Brak dostępnych pomiarów" in r.message for r in caplog.records)


def test_get_all_measurements_in_range_record_structure(measurements_dir, monkeypatch):
    monkeypatch.setattr("app.parser.MEASUREMENTS_PATH", measurements_dir)
    paths = [measurements_dir / "2023_PM10_1g.csv"]

    result = get_all_measurements_in_range(paths, datetime(2023, 1, 1), datetime(2023, 1, 1))

    assert all("station_code" in r for r in result)
    assert all("value" in r for r in result)
    assert all("timestamp" in r for r in result)
