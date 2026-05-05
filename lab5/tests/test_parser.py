import pytest
from pathlib import Path
from app.parser import parse_measurment, parse_stations


# --- parse_stations ---

def test_parse_stations_returns_station_codes_as_keys(stations_path):
    stations = parse_stations(stations_path)
    assert "DsBialka" in stations
    assert "MpKrakAlKras" in stations
    assert "SlKatoMOB" in stations


def test_parse_stations_parses_name_and_voivodeship(stations_path):
    stations = parse_stations(stations_path)
    bialka = stations["DsBialka"][0]
    assert bialka.nazwa_stacji == "Białka"
    assert bialka.wojewodztwo == "DOLNOŚLĄSKIE"


def test_parse_stations_parses_dates(stations_path):
    stations = parse_stations(stations_path)
    bialka = stations["DsBialka"][0]
    assert bialka.data_uruchomienia == "1990-01-03"
    assert bialka.data_zamkniecia == "2005-12-31"


def test_parse_stations_coordinates_stored_as_strings(stations_path):
    stations = parse_stations(stations_path)
    krak = stations["MpKrakAlKras"][0]
    assert krak.wgs84_n == "50.057678"
    assert krak.wgs84_e == "19.926189"


def test_parse_stations_empty_optional_fields_are_none(stations_path):
    stations = parse_stations(stations_path)
    bialka = stations["DsBialka"][0]
    assert bialka.kod_miedzynarodowy is None
    assert bialka.adres is None


def test_parse_stations_raises_for_missing_file():
    with pytest.raises(FileNotFoundError):
        parse_stations(Path("nonexistent.csv"))


# --- parse_measurment ---

def test_parse_measurment_groups_by_station_code(measurements_dir, monkeypatch):
    monkeypatch.setattr("app.parser.MEASUREMENTS_PATH", measurements_dir)
    result = parse_measurment(Path("2023_PM10_1g.csv"))
    assert "STA001" in result
    assert "STA002" in result


def test_parse_measurment_series_has_correct_fields(measurements_dir, monkeypatch):
    monkeypatch.setattr("app.parser.MEASUREMENTS_PATH", measurements_dir)
    result = parse_measurment(Path("2023_PM10_1g.csv"))
    series = result["STA001"][0]
    assert series.wskaznik == "PM10"
    assert series.czas_usredniania == "1g"
    assert series.jednostka == "ug/m3"
    assert series.kod_stanowiska == "STA001-PM10-1g"


def test_parse_measurment_parses_numeric_value(measurements_dir, monkeypatch):
    monkeypatch.setattr("app.parser.MEASUREMENTS_PATH", measurements_dir)
    result = parse_measurment(Path("2023_PM10_1g.csv"))
    first = result["STA001"][0].pomiary[0]
    assert first.timestamp == "01/01/23 01:00"
    assert first.value == pytest.approx(15.5)


def test_parse_measurment_empty_value_is_none(measurements_dir, monkeypatch):
    monkeypatch.setattr("app.parser.MEASUREMENTS_PATH", measurements_dir)
    result = parse_measurment(Path("2023_PM10_1g.csv"))
    second = result["STA001"][0].pomiary[1]
    assert second.value is None


def test_parse_measurment_raises_for_missing_file(measurements_dir, monkeypatch):
    monkeypatch.setattr("app.parser.MEASUREMENTS_PATH", measurements_dir)
    with pytest.raises(FileNotFoundError):
        parse_measurment(Path("nonexistent.csv"))
