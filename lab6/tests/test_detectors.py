from datetime import datetime

import numpy as np
import pytest

from app.detectors import OutlierDetector, SimpleReporter, ThresholdDetector, ZeroSpikeDetector
from app.timeseries import TimeSeries


def make_series(values: list[float | None]) -> TimeSeries:
    timestamps = [datetime(2023, 1, 1, h + 1) for h in range(len(values))]
    np_values = np.array([np.nan if v is None else v for v in values], dtype=float)
    return TimeSeries(
        sensor="PM10",
        code="StationA",
        averaging_time="1g",
        timestamps=timestamps,
        values=np_values,
        unit="ug/m3",
    )


# --- OutlierDetector ---

def test_outlier_detects_spike() -> None:
    # Use k=1.0 so the spike at 100 clearly exceeds 1 stddev from the mean
    values = [2.0, 2.0, 2.0, 100.0, 2.0]
    series = make_series(values)
    detector = OutlierDetector(k=1.0)
    results = detector.analyze(series)
    assert len(results) == 1
    assert "100" in results[0]


def test_outlier_no_anomaly() -> None:
    values = [1.0, 2.0, 3.0, 2.0, 1.0]
    series = make_series(values)
    detector = OutlierDetector(k=3.0)
    results = detector.analyze(series)
    assert results == []


def test_outlier_skips_nan() -> None:
    values = [1.0, None, 3.0]
    series = make_series(values)
    detector = OutlierDetector(k=0.1)
    results = detector.analyze(series)
    # None/nan should not appear in results
    for msg in results:
        assert "nan" not in msg.lower()


def test_outlier_all_none_returns_empty() -> None:
    series = make_series([None, None, None])
    detector = OutlierDetector(k=2.0)
    assert detector.analyze(series) == []


# --- ZeroSpikeDetector ---

def test_zero_spike_detects_3_zeros() -> None:
    series = make_series([1.0, 0.0, 0.0, 0.0, 1.0])
    detector = ZeroSpikeDetector()
    results = detector.analyze(series)
    assert len(results) == 1


def test_zero_spike_detects_nones() -> None:
    series = make_series([1.0, None, None, None, 1.0])
    detector = ZeroSpikeDetector()
    results = detector.analyze(series)
    assert len(results) == 1


def test_zero_spike_mixed_zeros_and_none() -> None:
    series = make_series([1.0, 0.0, None, 0.0, 1.0])
    detector = ZeroSpikeDetector()
    results = detector.analyze(series)
    assert len(results) == 1


def test_zero_spike_less_than_3_no_alert() -> None:
    series = make_series([1.0, 0.0, 0.0, 1.0])
    detector = ZeroSpikeDetector()
    results = detector.analyze(series)
    assert results == []


def test_zero_spike_no_zeros() -> None:
    series = make_series([1.0, 2.0, 3.0])
    detector = ZeroSpikeDetector()
    assert detector.analyze(series) == []


# --- ThresholdDetector ---

def test_threshold_detects_exceedance() -> None:
    series = make_series([10.0, 200.0, 5.0])
    detector = ThresholdDetector(threshold=100.0)
    results = detector.analyze(series)
    assert len(results) == 1
    assert "200" in results[0]


def test_threshold_no_exceedance() -> None:
    series = make_series([10.0, 50.0, 5.0])
    detector = ThresholdDetector(threshold=100.0)
    assert detector.analyze(series) == []


def test_threshold_skips_nan() -> None:
    series = make_series([None, 200.0])
    detector = ThresholdDetector(threshold=100.0)
    results = detector.analyze(series)
    assert len(results) == 1


# --- SimpleReporter (duck typing) ---

def test_simple_reporter_returns_info() -> None:
    series = make_series([1.0, 2.0, 3.0])
    reporter = SimpleReporter()
    results = reporter.analyze(series)
    assert len(results) == 1
    assert "Info" in results[0]
    assert "PM10" in results[0]
    assert "StationA" in results[0]


def test_simple_reporter_not_series_validator() -> None:
    from app.detectors import SeriesValidator
    reporter = SimpleReporter()
    assert not isinstance(reporter, SeriesValidator)


def test_duck_typing_mixed_list() -> None:
    """All analyzers must work when iterated without type checks."""
    series = make_series([1.0, 0.0, 0.0, 0.0, 500.0, 2.0])
    analyzers = [
        OutlierDetector(k=2.0),
        ZeroSpikeDetector(),
        ThresholdDetector(threshold=100.0),
        SimpleReporter(),
    ]
    for analyzer in analyzers:
        result = analyzer.analyze(series)
        assert isinstance(result, list)
