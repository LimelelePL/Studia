import re
from pathlib import Path

from app.constants import StationData
from app.parser import parse_stations

# TODO: przetestowac


# ul. chopina 10
def get_street_name(address: str) -> str:
    match = re.search(r"ul\.\s*([^\d]+)", address)
    return match.group(1).strip() if match else address


def get_house_number(address: str) -> str:
    match = re.search(r"(\d+[a-zA-Z]?)$", address)
    return match.group(1) if match else ""


def get_adresses(path: Path, city: str) -> list[tuple[str, str, str | None, str | None]]:
    if not path.is_file():
        raise FileNotFoundError("podany plik nie istnieje!")

    city_pattern = re.compile(rf"^{city}$", re.IGNORECASE)

    stations: dict[str, list[StationData]] = parse_stations(path)

    result = []
    for _, data in stations.items():
        if data := data[0]:
            is_matched = city_pattern.match(data.miejscowosc) is not None

            if is_matched:
                street = get_street_name(data.adres) if data.adres else None
                number = get_house_number(data.adres) if data.adres else None
                result.append((data.wojewodztwo, data.miejscowosc, street, number))

    return result
