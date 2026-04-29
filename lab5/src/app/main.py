from pathlib import Path

from app.constants import StationData, StationSeries
from app.parser import parse_measurment, parse_stations


def main() -> None:
    stations: dict[str, list[StationData]] = parse_stations()
    stats: dict[str, list[StationSeries]] = parse_measurment(Path("2023_NOx_1g.csv"))

    # print(stations["DsGlogMob"])
    print(stats["DsCzerStraza"][0].pomiary[0])


if __name__ == "__main__":
    main()
