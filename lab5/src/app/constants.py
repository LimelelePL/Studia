from dataclasses import dataclass
from enum import IntEnum, StrEnum
from pathlib import Path

STATIONS_PATH = Path("resources/stacje.csv")
MEASUREMENTS_PATH = Path("resources/measurements")


@dataclass
class StationData:
    nr: int
    kod_stacji: str
    kod_miedzynarodowy: str | None
    nazwa_stacji: str
    stary_kod_stacji: str | None
    data_uruchomienia: str | None
    data_zamkniecia: str | None
    typ_stacji: str
    typ_obszaru: str
    rodzaj_stacji: str
    wojewodztwo: str
    miejscowosc: str
    adres: str | None
    wgs84_n: str
    wgs84_e: str


class StationEntry(StrEnum):
    nr = "Nr"
    kod_stacji = "Kod stacji"
    kod_int = "Kod międzynarodowy"
    nazwa = "Nazwa stacji"
    stary_kod = "Stary Kod stacji \n(o ile inny od aktualnego)"
    data_uruchomienia = "Data uruchomienia"
    data_zamkniecia = "Data zamknięcia"
    typ_stacji = "Typ stacji"
    typ_obszaru = "Typ obszaru"
    rodzaj_stacji = "Rodzaj stacji"
    wojewodztwo = "Województwo"
    miejscowosc = "Miejscowość"
    adres = "Adres"
    WGS84_N = "WGS84 φ N"
    WGS84_E = "WGS84 λ E"


class MeasurementsRawEntry(IntEnum):
    nr = 0
    kod_stacji = 1
    wskaznik = 2
    czas_usrednienia = 3
    jednostka = 4
    kod_stanowiska = 5
    dane = 6  # dane od 6 miejsca do konca


@dataclass
class SingeMeasurement:
    timestamp: str
    value: float | None


@dataclass
class StationSeries:
    kod_stacji: str
    wskaznik: str
    jednostka: str
    czas_usredniania: str
    kod_stanowiska: str
    pomiary: list[SingeMeasurement]
