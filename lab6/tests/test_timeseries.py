import math
from datetime import date, datetime

import numpy as np
import pytest

from app.timeseries import TimeSeries


def make_series(values: list[float | None] | None = None) -> TimeSeries:
    if values is None:
        values = [1.0, 2.0, 3.0, 4.0, 5.0]
    timestamps = [datetime(2023, 1, 1, h + 1) for h in range(len(values))]
    np_values = np.array([np.nan if v is None else v for v in values], dtype=float)
    return TimeSeries(
        sensor="C6H6",
        code="TestStation",
        averaging_time="1g",
        timestamps=timestamps,
        values=np_values,
        unit="ug/m3",
    )


def test_init_length_mismatch() -> None:
    with pytest.raises(ValueError):
        TimeSeries(
            sensor="C6H6",
            code="X",
            averaging_time="1g",
            timestamps=[datetime(2023, 1, 1)],
            values=np.array([1.0, 2.0]),
            unit="ug/m3",
        )


def test_getitem_int() -> None:
    series = make_series([10.0, 20.0, 30.0])
    ts, val = series[0]
    assert ts == datetime(2023, 1, 1, 1)
    assert val == 10.0


def test_getitem_slice() -> None:
    series = make_series([10.0, 20.0, 30.0])
    result = series[0:2]
    assert len(result) == 2
    assert result[0] == (datetime(2023, 1, 1, 1), 10.0)
    assert result[1] == (datetime(2023, 1, 1, 2), 20.0)


def test_getitem_datetime_found() -> None:
    series = make_series([10.0, 20.0])
    val = series[datetime(2023, 1, 1, 1)]
    assert val == 10.0


def test_getitem_datetime_not_found() -> None:
    series = make_series([10.0])
    with pytest.raises(KeyError):
        series[datetime(2099, 12, 31, 0)]


def test_getitem_date_found() -> None:
    series = make_series([10.0, 20.0])
    result = series[date(2023, 1, 1)]
    # Two measurements on that date → list
    assert isinstance(result, list)
    assert len(result) == 2


def test_getitem_date_not_found() -> None:
    series = make_series([10.0])
    with pytest.raises(KeyError):
        series[date(2099, 12, 31)]


def test_getitem_invalid_type() -> None:
    series = make_series([1.0])
    with pytest.raises(TypeError):
        series["invalid"]  # type: ignore[index]


def test_mean_normal() -> None:
    series = make_series([2.0, 4.0, 6.0])
    assert series.mean == pytest.approx(4.0)


def test_mean_with_none() -> None:
    series = make_series([2.0, None, 6.0])
    assert series.mean == pytest.approx(4.0)


def test_mean_all_none() -> None:
    series = make_series([None, None])
    assert series.mean is None


def test_stddev_normal() -> None:
    series = make_series([2.0, 4.0, 6.0])
    assert series.stddev is not None
    assert series.stddev > 0


def test_stddev_all_none() -> None:
    series = make_series([None, None])
    assert series.stddev is None


def test_stddev_single_value() -> None:
    series = make_series([5.0])
    assert series.stddev == pytest.approx(0.0)
