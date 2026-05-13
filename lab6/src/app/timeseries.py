from datetime import date, datetime

import numpy as np


class TimeSeries:
    def __init__(
        self,
        sensor: str,
        code: str,
        averaging_time: str,
        timestamps: list[datetime],
        values: np.ndarray,
        unit: str,
    ) -> None:
        if len(timestamps) != len(values):
            raise ValueError("timestamps i values musza miec taka sama dlugosc")

        self.sensor = sensor
        self.code = code
        self.averaging_time = averaging_time
        self.timestamps = timestamps
        self.values = values
        self.unit = unit

    def __getitem__(
        self, key: int | slice | datetime | date
    ) -> tuple[datetime, float | None] | list[tuple[datetime, float | None]] | float | list[float | None] | None:
        matched_values: list[float | None] = []
        match key:
            case int():
                return (self.timestamps[key], self.values[key])

            case slice():
                return list(zip(self.timestamps[key], self.values[key], strict=False))

            case datetime():
                for timestamp, value in zip(self.timestamps, self.values, strict=False):
                    if timestamp == key:
                        matched_values.append(value)

                if not matched_values:
                    raise KeyError(key)

                if len(matched_values) == 1:
                    return matched_values[0]

                return matched_values

            case date():
                for timestamp, value in zip(self.timestamps, self.values, strict=False):
                    if timestamp.date() == key:
                        matched_values.append(value)

                if not matched_values:
                    raise KeyError(key)

                if len(matched_values) == 1:
                    return matched_values[0]

                return matched_values

            case _:
                raise TypeError("key musi byc int, slice, datetime albo date")

    @property
    def mean(self) -> float | None:
        if np.isnan(self.values).all():
            return None
        return float(np.nanmean(self.values))

    @property
    def stddev(self) -> float | None:
        if np.isnan(self.values).all():
            return None
        return float(np.nanstd(self.values))

    @property
    def min_value(self) -> float | None:
        if np.isnan(self.values).all():
            return None

        return np.min(self.values)

    @property
    def max_value(self) -> float | None:
        if np.isnan(self.values).all():
            return None

        return np.max(self.values)
