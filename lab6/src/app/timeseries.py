from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class TimeSeries:
    sensor: str
    code: str
    averaging_time: str
    timestamps: list[datetime]
    values: list[float | None]
    unit: str

    def __init__(
        self,
        sensor: str,
        code: str,
        averaging_time: str,
        timestamps: list[datetime],
        values: list[float | None],
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
        if isinstance(key, int):
            return (self.timestamps[key], self.values[key])

        if isinstance(key, slice):
            return list(zip(self.timestamps[key], self.values[key], strict=False))

        if isinstance(key, datetime):
            matched_values = [
                value for timestamp, value in zip(self.timestamps, self.values, strict=False) if timestamp == key
            ]

            if not matched_values:
                raise KeyError(key)

            if len(matched_values) == 1:
                return matched_values[0]

            return matched_values

        if isinstance(key, date):
            matched_values = [
                value for timestamp, value in zip(self.timestamps, self.values, strict=False) if timestamp.date() == key
            ]

            if not matched_values:
                raise KeyError(key)

            if len(matched_values) == 1:
                return matched_values[0]

            return matched_values

        raise TypeError("key musi byc int, slice, datetime albo date")
