import pytest
from pathlib import Path
from app.get_addresses import get_adresses


def test_returns_address_tuples_for_matching_city(stations_path):
    result = get_adresses(stations_path, "Kraków")
    assert len(result) == 1
    voivodeship, city, street, number = result[0]
    assert voivodeship == "MAŁOPOLSKIE"
    assert city == "Kraków"
    assert street == "Krasińskiego"
    assert number == "1"


def test_returns_empty_list_for_unknown_city(stations_path):
    result = get_adresses(stations_path, "Wrocław")
    assert result == []


def test_city_matching_is_case_insensitive(stations_path):
    assert len(get_adresses(stations_path, "kraków")) == 1
    assert len(get_adresses(stations_path, "KRAKÓW")) == 1


def test_station_without_address_returns_none_fields(stations_path):
    result = get_adresses(stations_path, "Białka")
    assert len(result) == 1
    _, _, street, number = result[0]
    assert street is None
    assert number is None


def test_raises_for_missing_file():
    with pytest.raises(FileNotFoundError):
        get_adresses(Path("nonexistent.csv"), "Kraków")
