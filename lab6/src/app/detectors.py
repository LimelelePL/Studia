from abc import ABC, abstractmethod

import numpy as np

from app.timeseries import TimeSeries


class SeriesValidator(ABC):
    @abstractmethod
    def analyze(self, series: TimeSeries) -> list[str]:
        pass


class OutlierDetector(SeriesValidator):
    def __init__(self, k: float) -> None:
        self.k = k

    def analyze(self, series: TimeSeries) -> list[str]:
        if series.mean is None or series.stddev is None:
            return []

        mean = series.mean
        stddev = series.stddev

        if stddev == 0:
            return []

        result: list[str] = []

        for timestamp, value in zip(series.timestamps, series.values, strict=False):
            if value is None or np.isnan(value):
                continue

            if abs(value - mean) > self.k * stddev:
                result.append(
                    f"Outlier dla stacji {series.code}, wskaznika {series.sensor}: "
                    f"{value} w czasie {timestamp.isoformat()}"
                )

        return result


class ZeroSpikeDetector(SeriesValidator):
    def analyze(self, series: TimeSeries) -> list[str]:
        min_number_of_zeros = 3
        number_of_zeros_or_none = 0
        start_timestamp = None
        previous_timestamp = None

        result: list[str] = []

        def is_end_of_sequence() -> bool:
            return number_of_zeros_or_none >= min_number_of_zeros

        def append_message() -> None:
            if start_timestamp is not None and previous_timestamp is not None:
                result.append(
                    f"ZeroSpikeDetector dla stacji {series.code}, wskaznika {series.sensor}: "
                    f"{number_of_zeros_or_none} zer lub brakow danych z rzedu "
                    f"od {start_timestamp.isoformat()} do {previous_timestamp.isoformat()}"
                )

        for timestamp, value in zip(series.timestamps, series.values, strict=False):
            if value is None or np.isnan(value) or value == 0:
                if number_of_zeros_or_none == 0:
                    start_timestamp = timestamp

                number_of_zeros_or_none += 1
                previous_timestamp = timestamp
                continue

            if is_end_of_sequence():
                append_message()

            number_of_zeros_or_none = 0
            start_timestamp = None
            previous_timestamp = timestamp

        if is_end_of_sequence():
            append_message()

        return result


class ThresholdDetector(SeriesValidator):
    def __init__(self, threshold: float) -> None:
        self.threshold = threshold

    def analyze(self, series: TimeSeries) -> list[str]:
        result: list[str] = []

        for timestamp, value in zip(series.timestamps, series.values, strict=False):
            if value is None or np.isnan(value):
                continue

            if value > self.threshold:
                result.append(
                    f"ThresholdDetector dla stacji {series.code}, wskaznika {series.sensor}: "
                    f"{value} przekracza prog {self.threshold} w czasie {timestamp.isoformat()}"
                )

        return result


class SimpleReporter:
    """Słuzy do pokazania "kaczego" typowanie: nie dziediczy po SeriesValidator ale posiada metode analyzce()."""

    def analyze(self, series: TimeSeries) -> list[str]:
        return [f"Info: {series.sensor} at {series.code} has mean = {series.mean}"]
