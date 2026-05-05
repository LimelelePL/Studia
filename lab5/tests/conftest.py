import pytest
from pathlib import Path
from app.constants import StationData

STATIONS_CSV = """\
Nr,Kod stacji,Kod międzynarodowy,Nazwa stacji,"Stary Kod stacji \n(o ile inny od aktualnego)",Data uruchomienia,Data zamknięcia,Typ stacji,Typ obszaru,Rodzaj stacji,Województwo,Miejscowość,Adres,WGS84 φ N,WGS84 λ E
1,DsBialka,,Białka,,1990-01-03,2005-12-31,przemysłowa,podmiejski,kontenerowa stacjonarna,DOLNOŚLĄSKIE,Białka,,51.197783,16.117390
2,MpKrakAlKras,,Kraków - al. Krasińskiego,,2000-05-15,,tła miejskiego,miejski,automatyczna,MAŁOPOLSKIE,Kraków,ul. Krasińskiego 1,50.057678,19.926189
3,SlKatoMOB,,Katowice - mobilna,,2010-01-01,,mobilna,miejski,mobilna,ŚLĄSKIE,Katowice,al. Roździeńskiego 10,50.260000,19.020000
"""

MEASUREMENT_CSV = """\
Nr,1,2
Kod stacji,STA001,STA002
Wskaźnik,PM10,PM10
Czas uśredniania,1g,1g
Jednostka,ug/m3,ug/m3
Kod stanowiska,STA001-PM10-1g,STA002-PM10-1g
01/01/23 01:00,15.5,20.3
01/01/23 02:00,,8.7
"""


@pytest.fixture
def station_factory():
    def _make(**kwargs) -> StationData:
        defaults: dict = dict(
            nr=1,
            kod_stacji="TEST001",
            kod_miedzynarodowy=None,
            nazwa_stacji="Test Station",
            stary_kod_stacji=None,
            data_uruchomienia="2000-01-01",
            data_zamkniecia="",
            typ_stacji="tła miejskiego",
            typ_obszaru="miejski",
            rodzaj_stacji="automatyczna",
            wojewodztwo="MAŁOPOLSKIE",
            miejscowosc="Kraków",
            adres=None,
            wgs84_n="50.057678",
            wgs84_e="19.926189",
        )
        defaults.update(kwargs)
        return StationData(**defaults)

    return _make


@pytest.fixture
def stations_path(tmp_path: Path) -> Path:
    path = tmp_path / "stacje.csv"
    path.write_text(STATIONS_CSV, encoding="utf-8")
    return path


@pytest.fixture
def measurements_dir(tmp_path: Path) -> Path:
    mdir = tmp_path / "measurements"
    mdir.mkdir()
    (mdir / "2023_PM10_1g.csv").write_text(MEASUREMENT_CSV, encoding="utf-8")
    return mdir
