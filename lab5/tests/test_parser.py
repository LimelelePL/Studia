from app.constants import MEASUREMENTS_PATH
from app.parser import parse_measurment, parse_measurements, parse_stations


def test_parse_stations_reads_utf8_headers_and_groups_duplicates() -> None:
    stations = parse_stations()

    assert "DsBialka" in stations
    assert stations["DsBialka"][0].nazwa_stacji == "Białka"
    assert stations["DsBialka"][0].wojewodztwo == "DOLNOŚLĄSKIE"


def test_parse_measurements_groups_many_series_for_same_station() -> None:
    measurements = parse_measurements()

    assert "DsJelGorOgin" in measurements

    indicators = {series.wskaznik for series in measurements["DsJelGorOgin"]}
    assert {"SO2", "CO", "NO2"} <= indicators

    so2_series = next(series for series in measurements["DsJelGorOgin"] if series.wskaznik == "SO2")
    assert so2_series.kod_stanowiska == "DsJelGorOgin-SO2-1g"
    assert so2_series.data[0].timestamp == "01/01/23 01:00"
    assert so2_series.data[0].value == 8.2317099999999996


def test_parse_measurement_handles_shifted_site_code_row() -> None:
    measurements = parse_measurment(MEASUREMENTS_PATH / "2023_NO2_1g.csv")

    no2_series = next(series for series in measurements["DsJelGorOgin"] if series.wskaznik == "NO2")
    assert no2_series.kod_stanowiska == "DsJelGorOgin-NO2-1g"
    assert no2_series.data[0].timestamp == "01/01/23 01:00"


def test_parse_measurement_handles_period_file() -> None:
    measurements = parse_measurment(MEASUREMENTS_PATH / "2023_Depozycja_1m.csv")

    series = measurements["DsOsieczow21"][0]
    assert series.data[0].timestamp == "01/01/23 12:00 -> 2023-01-01 24:00"
