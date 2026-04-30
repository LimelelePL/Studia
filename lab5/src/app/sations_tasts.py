import copy
import re

from app.constants import StationData

# TODO zrobic f i g


# 2001-12-31
def is_date(date: str) -> bool:
    pattern = re.compile(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$")
    return bool(pattern.match(date))


def find_dates(stations: dict[str, list[StationData]]) -> list[tuple[str, str]]:
    result = set()
    for _, data in stations.items():
        for d in data:
            start_date = d.data_uruchomienia.strip() if d.data_uruchomienia else ""
            close_date = d.data_zamkniecia.strip() if d.data_zamkniecia else ""

            if is_date(start_date) and is_date(close_date):
                result.add((start_date, close_date))

    return list(result)


def is_coordinate(coordinate: str) -> bool:
    pattern = re.compile(r"\d{2}\.\d{6}")
    return bool(pattern.match(coordinate))


def find_coordinates(stations: dict[str, list[StationData]]) -> list[tuple[str, str]]:
    result = set()
    for _, data in stations.items():
        for d in data:
            lon = d.wgs84_e.strip()
            lat = d.wgs84_n.strip()

            if is_coordinate(lon) and is_coordinate(lat):
                result.add((lon, lat))

    return list(result)


def is_with_dash(name: str) -> bool:
    pattern = re.compile(r".+-.+")
    return bool(pattern.match(name))


def find_stations_with_dash(stations: dict[str, list[StationData]]) -> list[str]:
    result = set()
    for _, data in stations.items():
        for d in data:
            name = d.nazwa_stacji
            if is_with_dash(name):
                result.add(name)

    return list(result)


def change_space_to_(name: str) -> str:
    return re.sub(r"\s+", "_", name.strip())


def change_polish_special_alpha(name: str) -> str:
    for pl, lat in zip("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ", "acelnoszzACELNOSZZ"):
        res = re.sub(pl, lat, name.strip())
    return res


def convert_station_names(stations: dict[str, list[StationData]]) -> dict[str, list[StationData]]:
    stations_copy = copy.deepcopy(stations)
    for _, data in stations.items():
        for d in data:
            name = d.nazwa_stacji
            name = change_space_to_(name)
            name = change_polish_special_alpha(name)
            d.nazwa_stacji = name
    return stations_copy


def has_mob_ending(name: str) -> bool:
    pattern = re.compile(r"mob$", flags=re.IGNORECASE)
    return bool(pattern.search(name.strip()))


def verify_mob_ending(stations: dict[str, list[StationData]]) -> bool:
    for _, data in stations.items():
        for d in data:
            name = d.nazwa_stacji.lower()
            type_s = d.rodzaj_stacji.lower()
            if has_mob_ending(name) and type_s.strip() != "mobilna":
                return False
    return True
