from app.station import Station


def make_station(code: str = "ABC123", name: str = "Test Station") -> Station:
    return Station(
        code=code,
        international_code=None,
        name=name,
        old_code=None,
        opening_time="2000-01-01",
        closing_time=None,
        station_type="tla",
        area_type="miejski",
        station_category="automatyczna",
        province="DOLNOŚLĄSKIE",
        locality="Wrocław",
        address="ul. Testowa 1",
        latitude="51.1",
        longitude="17.0",
    )


def test_eq_same_code() -> None:
    s1 = make_station(code="ABC")
    s2 = make_station(code="ABC", name="Inny")
    assert s1 == s2


def test_eq_different_code() -> None:
    s1 = make_station(code="ABC")
    s2 = make_station(code="XYZ")
    assert s1 != s2


def test_eq_non_station() -> None:
    s = make_station(code="ABC")
    assert s != "ABC"
    assert s != 42


def test_str_contains_name_and_code() -> None:
    s = make_station(code="ABC123", name="Stacja Testowa")
    result = str(s)
    assert "ABC123" in result
    assert "Stacja Testowa" in result


def test_repr_contains_code() -> None:
    s = make_station(code="ABC123")
    result = repr(s)
    assert "ABC123" in result
