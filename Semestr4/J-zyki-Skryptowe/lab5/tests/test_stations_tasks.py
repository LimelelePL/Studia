import pytest
from app.sations_tasts import (
    change_polish_special_alpha,
    change_space_to_,
    find_coordinates,
    find_dates,
    find_stations_with_dash,
    find_stations_with_three_sashes,
    find_stations_with_ul_or_al,
    has_name_with_three_dashes,
    has_ul_or_al,
    is_coordinate,
    is_date,
    is_with_dash,
    verify_mob_ending,
)


# --- is_date ---

@pytest.mark.parametrize("date", ["2000-01-01", "2023-12-31", "1990-06-15"])
def test_is_date_valid(date):
    assert is_date(date) is True


@pytest.mark.parametrize("date", ["2000-13-01", "2000-00-01", "2000-1-1", "not-a-date", ""])
def test_is_date_invalid(date):
    assert is_date(date) is False


# --- find_dates ---

def test_find_dates_returns_valid_pairs(station_factory):
    stations = {
        "S1": [station_factory(data_uruchomienia="2000-01-01", data_zamkniecia="2023-12-31")],
        "S2": [station_factory(data_uruchomienia="", data_zamkniecia="")],
    }
    result = find_dates(stations)
    assert ("2000-01-01", "2023-12-31") in result
    assert len(result) == 1


# --- is_coordinate ---

@pytest.mark.parametrize("coord", ["50.057678", "19.926189", "51.123456"])
def test_is_coordinate_valid(coord):
    assert is_coordinate(coord) is True


@pytest.mark.parametrize("coord", ["50.12345", "50.1234567", "abc", "50,123456"])
def test_is_coordinate_invalid(coord):
    assert is_coordinate(coord) is False


# --- find_coordinates ---

def test_find_coordinates_returns_valid_pairs(station_factory):
    stations = {
        "S1": [station_factory(wgs84_n="50.057678", wgs84_e="19.926189")],
        "S2": [station_factory(wgs84_n="bad", wgs84_e="bad")],
    }
    result = find_coordinates(stations)
    assert ("19.926189", "50.057678") in result
    assert len(result) == 1


# --- is_with_dash ---

@pytest.mark.parametrize("name", ["Bogatynia - Chopina", "Bielawa - ul. Grota", "A-B"])
def test_is_with_dash_true(name):
    assert is_with_dash(name) is True


def test_is_with_dash_false():
    assert is_with_dash("Białka") is False


# --- change_space_to_ ---

def test_change_space_to_underscore():
    assert change_space_to_("Hello World") == "Hello_World"


def test_change_space_to_underscore_multiple_spaces():
    assert change_space_to_("A  B  C") == "A_B_C"


def test_change_space_to_underscore_trims():
    assert change_space_to_("  text  ") == "text"


# --- change_polish_special_alpha ---

def test_change_polish_special_alpha_replaces_all():
    # Ten test ujawnia buga: petla nadpisuje 'res' i efektywnie zamienia tylko ostatni znak
    assert change_polish_special_alpha("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ") == "acelnoszzACELNOSZZ"


# --- verify_mob_ending ---

def test_verify_mob_ending_passes_when_mob_is_mobile(station_factory):
    stations = {"SlKatoMOB": [station_factory(nazwa_stacji="Katowice MOB", rodzaj_stacji="mobilna")]}
    assert verify_mob_ending(stations) is True


def test_verify_mob_ending_fails_when_mob_is_not_mobile(station_factory):
    stations = {"SlKatoMOB": [station_factory(nazwa_stacji="Katowice MOB", rodzaj_stacji="automatyczna")]}
    assert verify_mob_ending(stations) is False


def test_verify_mob_ending_ignores_stations_without_mob(station_factory):
    stations = {"MpKrak": [station_factory(nazwa_stacji="Kraków", rodzaj_stacji="automatyczna")]}
    assert verify_mob_ending(stations) is True


# --- has_name_with_three_dashes ---

@pytest.mark.parametrize("name", ["Abc-Def-Ghi", "A1-B2-C3"])
def test_has_three_dashes_true(name):
    assert has_name_with_three_dashes(name) is True


@pytest.mark.parametrize("name", ["Abc-Def", "Abc", "Abc-Def-Ghi-Jkl"])
def test_has_three_dashes_false(name):
    assert has_name_with_three_dashes(name) is False


# --- has_ul_or_al ---

def test_has_ul_matches():
    assert has_ul_or_al("Głogów, ul. Orzechowa") is True


def test_has_al_matches():
    # Ten test ujawnia buga: pattern obsluguje tylko 'ul.', nie 'al.'
    assert has_ul_or_al("Kraków, al. Krasińskiego") is True


# --- find_stations_with_dash ---

def test_find_stations_with_dash(station_factory):
    stations = {
        "S1": [station_factory(nazwa_stacji="Bogatynia - Chopina")],
        "S2": [station_factory(nazwa_stacji="Białka")],
    }
    result = find_stations_with_dash(stations)
    assert "Bogatynia - Chopina" in result
    assert "Białka" not in result


# --- find_stations_with_three_sashes ---

def test_find_stations_with_three_sashes(station_factory):
    stations = {
        "S1": [station_factory(nazwa_stacji="Abc-Def-Ghi")],
        "S2": [station_factory(nazwa_stacji="Abc-Def")],
    }
    result = find_stations_with_three_sashes(stations)
    assert "Abc-Def-Ghi" in result
    assert "Abc-Def" not in result


# --- find_stations_with_ul_or_al ---

def test_find_stations_with_ul(station_factory):
    stations = {
        "S1": [station_factory(nazwa_stacji="Głogów, ul. Orzechowa")],
        "S2": [station_factory(nazwa_stacji="Białka")],
    }
    result = find_stations_with_ul_or_al(stations)
    assert "Głogów, ul. Orzechowa" in result
    assert "Białka" not in result
