from app.constants import STATIONS_PATH
from app.parser import parse_stations
from app.sations_tasts import *


def main() -> None:
    stations: dict[str, list[StationData]] = parse_stations(STATIONS_PATH)
    # stats: dict[str, list[StationSeries]] = parse_measurment(Path("2023_NOx_1g.csv"))
    # print(find_dates(stations))
    # print(find_coordinates(stations))
    # print(find_stations_with_dash(stations))
    # print(verify_mob_ending(stations))
    print(find_stations_with_ul_or_al(stations))
    # print(find_stations_with_three_sashes(stations))
a

if __name__ == "__main__":
    main()
