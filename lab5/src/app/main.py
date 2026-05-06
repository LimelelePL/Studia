from app.constants import STATIONS_PATH
from app.parser import parse_stations
from app.sations_tasts import find_stations_with_ul_or_al


def main() -> None:
    stations = parse_stations(STATIONS_PATH)
    print(find_stations_with_ul_or_al(stations))


if __name__ == "__main__":
    main()
