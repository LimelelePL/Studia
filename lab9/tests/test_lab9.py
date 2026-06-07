import csv
import tempfile
from collections.abc import Iterator
from datetime import date, datetime
from pathlib import Path
from typing import cast

import numpy as np
import pytest

from app.detectors import OutlierDetector, SeriesAnalyzer, SimpleReporter, ThresholdDetector, ZeroSpikeDetector
from app.measurements import Measurements
from app.station import Station
from app.timeseries import TimeSeries


def make_station(code: str = "ABC", name: str = "Test Station") -> Station:
    return Station(
        code=code,
        international_code=None,
        name=name,
        old_code=None,
        opening_time="2023-01-01",
        closing_time=None,
        station_type="tlo",
        area_type="miejski",
        station_category="automatyczna",
        province="DOLNOSLASKIE",
        locality="Wroclaw",
        address="ul. Testowa 1",
        latitude="51.100000",
        longitude="17.000000",
    )


def make_series(values: list[float | None] | None = None) -> TimeSeries:
    if values is None:
        values = [1.0, 2.0, 3.0]

    return TimeSeries(
        sensor="PM10",
        code="StationA",
        averaging_time="1g",
        timestamps=[datetime(2023, 1, 1, hour + 1) for hour in range(len(values))],
        values=np.array(values, dtype=np.float64),
        unit="ug/m3",
    )


def write_measurements_csv(path: Path, rows: list[list[str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Nr", "1"])
        writer.writerow(["Kod stacji", "StationA"])
        writer.writerow(["Wskaznik", "PM10"])
        writer.writerow(["Czas usredniania", "1g"])
        writer.writerow(["Jednostka", "ug/m3"])
        writer.writerow(["Kod stanowiska", "StationA-PM10-1g"])
        writer.writerows(rows)


@pytest.fixture
def measurements_dir() -> Iterator[Path]:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp)
        write_measurements_csv(
            path / "2023_PM10_1g.csv",
            [
                ["01/01/23 01:00", "1.0"],
                ["01/01/23 02:00", "0.0"],
                ["01/01/23 03:00", "0.0"],
                ["01/01/23 04:00", "0.0"],
                ["01/01/23 05:00", "100.0"],
            ],
        )
        yield path


def test_station_eq_uses_station_code() -> None:
    assert make_station(code="ABC", name="One") == make_station(code="ABC", name="Two")
    assert make_station(code="ABC") != make_station(code="XYZ")


def test_timeseries_getitem_int() -> None:
    timestamp, value = cast(tuple[datetime, float | None], make_series([10.0, 20.0])[0])
    assert timestamp == datetime(2023, 1, 1, 1)
    assert value == pytest.approx(10.0)


def test_timeseries_getitem_slice() -> None:
    assert make_series([10.0, 20.0, 30.0])[1:] == [
        (datetime(2023, 1, 1, 2), 20.0),
        (datetime(2023, 1, 1, 3), 30.0),
    ]


def test_timeseries_getitem_existing_date() -> None:
    result = make_series([10.0, 20.0])[date(2023, 1, 1)]
    assert result == [10.0, 20.0]


def test_timeseries_getitem_missing_date_raises_key_error() -> None:
    with pytest.raises(KeyError):
        make_series([10.0])[date(2023, 1, 2)]


def test_timeseries_mean_and_stddev_complete_data() -> None:
    series = make_series([2.0, 4.0, 6.0])
    assert series.mean == pytest.approx(4.0)
    assert series.stddev == pytest.approx(np.std([2.0, 4.0, 6.0]))


def test_timeseries_mean_and_stddev_ignore_none_values() -> None:
    series = make_series([2.0, None, 6.0])
    assert series.mean == pytest.approx(4.0)
    assert series.stddev == pytest.approx(np.std([2.0, 6.0]))


def test_outlier_detector_reports_outlier() -> None:
    results = OutlierDetector(k=1.0).analyze(make_series([2.0, 2.0, 2.0, 100.0, 2.0]))
    assert len(results) == 1
    assert "100" in results[0]


def test_zero_spike_detector_reports_three_consecutive_zeros_or_none() -> None:
    zero_results = ZeroSpikeDetector().analyze(make_series([1.0, 0.0, 0.0, 0.0, 1.0]))
    none_results = ZeroSpikeDetector().analyze(make_series([1.0, None, None, None, 1.0]))

    assert len(zero_results) == 1
    assert len(none_results) == 1


def test_threshold_detector_reports_values_above_threshold() -> None:
    results = ThresholdDetector(threshold=50.0).analyze(make_series([10.0, 60.0, 20.0]))
    assert len(results) == 1
    assert "60" in results[0]


@pytest.mark.parametrize(
    "analyzer",
    [
        OutlierDetector(k=1.0),
        ZeroSpikeDetector(),
        ThresholdDetector(threshold=50.0),
        SimpleReporter(),
    ],
)
def test_analyzers_return_message_lists_without_type_checks(analyzer: SeriesAnalyzer) -> None:
    result = analyzer.analyze(make_series([1.0, 0.0, 0.0, 0.0, 100.0]))
    assert result == list(result)
    assert "\n".join(result) == "\n".join(str(message) for message in result)


@pytest.mark.parametrize(
    "analyzer",
    [
        OutlierDetector(k=1.0),
        ZeroSpikeDetector(),
        ThresholdDetector(threshold=50.0),
        SimpleReporter(),
    ],
)
def test_detect_all_anomalies_accepts_structural_analyzers(analyzer: SeriesAnalyzer, measurements_dir: Path) -> None:
    measurements = Measurements(measurements_dir)
    results = measurements.detect_all_anomalies([analyzer], preload=True)

    assert set(results) == {"StationA_PM10"}
    assert results["StationA_PM10"] == list(results["StationA_PM10"])
