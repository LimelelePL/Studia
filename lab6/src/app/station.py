from dataclasses import dataclass


@dataclass
class Station:
    code: str
    international_code: str | None
    name: str
    old_code: str | None
    opening_time: str | None
    closing_time: str | None
    station_type: str
    area_type: str
    station_category: str
    province: str
    locality: str
    address: str | None
    latitude: str
    longitude: str

    def __init__(
        self,
        code: str,
        international_code: str | None,
        name: str,
        old_code: str | None,
        opening_time: str | None,
        closing_time: str | None,
        station_type: str,
        area_type: str,
        station_category: str,
        province: str,
        locality: str,
        address: str | None,
        latitude: str,
        longitude: str,
    ):
        self.code = code
        self.international_code = international_code
        self.name = name
        self.old_code = old_code
        self.opening_time = opening_time
        self.closing_time = closing_time
        self.station_type = station_type
        self.area_type = area_type
        self.station_category = station_category
        self.province = province
        self.locality = locality
        self.address = address
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self) -> str:
        return (
            f"Station(name: {self.name}, code: {self.code}, station_type: {self.station_type},address: {self.address})"
        )

    def __repr__(self) -> str:
        return (
            f"Station(code={self.code!r}, station_type={self.international_code!r}, "
            f"name={self.name!r}, address={self.address!r})"
        )

    def __eq__(self, other: "Station") -> bool:
        return self.code == other.code
