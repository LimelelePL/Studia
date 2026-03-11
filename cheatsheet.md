# Python Cheatsheet

## Typy i Type Hints

```python
# Podstawowe typy
x: int = 1
y: float = 1.0
z: str = "hello"
b: bool = True

# Kolekcje
lista: list[int] = [1, 2, 3]
slownik: dict[str, int] = {"a": 1, "b": 2}
zbior: set[int] = {1, 2, 3}
krotka: tuple[int, str, float] = (1, "a", 1.0)

# Opcjonalne wartości
from typing import Optional
imie: Optional[str] = None  # może być str lub None
imie: str | None = None     # nowszy zapis (Python 3.10+)

# Union — kilka możliwych typów
from typing import Union
wartosc: Union[int, str] = 1
wartosc: int | str = 1      # nowszy zapis

# Any — dowolny typ (unikaj!)
from typing import Any
cokolwiek: Any = "cokolwiek"

# Callable — funkcja jako typ
from typing import Callable
func: Callable[[int, int], float] = calculate_area
```

---

## Funkcje

```python
# Podstawowa funkcja
def dodaj(a: int, b: int) -> int:
    return a + b

# Domyślne argumenty
def powitaj(imie: str, prefix: str = "Cześć") -> str:
    return f"{prefix}, {imie}!"

# Argumenty keyword-only (po *)
def stworz_usera(imie: str, *, admin: bool = False) -> dict:
    return {"imie": imie, "admin": admin}

stworz_usera("Jan", admin=True)   # OK
stworz_usera("Jan", True)         # błąd!

# Dowolna liczba argumentów
def suma(*args: int) -> int:
    return sum(args)

suma(1, 2, 3, 4)  # 10

# Dowolna liczba argumentów keyword
def loguj(**kwargs: str) -> None:
    for key, value in kwargs.items():
        print(f"{key}: {value}")

loguj(imie="Jan", wiek="25")

# Lambda — anonimowa funkcja
kwadrat = lambda x: x ** 2
kwadrat(5)  # 25
```

---

## Klasy

```python
from dataclasses import dataclass


# Podstawowa klasa
class Trojkat:
    def __init__(self, podstawa: float, wysokosc: float) -> None:
        self.podstawa = podstawa
        self.wysokosc = wysokosc

    def pole(self) -> float:
        return (self.podstawa * self.wysokosc) / 2

    def __repr__(self) -> str:
        return f"Trojkat(podstawa={self.podstawa}, wysokosc={self.wysokosc})"

    def __str__(self) -> str:
        return f"Trójkąt o polu {self.pole()}"


# Dataclass — krótszy zapis, przydatny dla prostych klas
@dataclass
class Punkt:
    x: float
    y: float
    z: float = 0.0  # domyślna wartość

p = Punkt(1.0, 2.0)
print(p)  # Punkt(x=1.0, y=2.0, z=0.0)


# Dziedziczenie
class Figura:
    def pole(self) -> float:
        raise NotImplementedError

class Prostokat(Figura):
    def __init__(self, a: float, b: float) -> None:
        self.a = a
        self.b = b

    def pole(self) -> float:
        return self.a * self.b


# Klasa abstrakcyjna
from abc import ABC, abstractmethod

class Figura(ABC):
    @abstractmethod
    def pole(self) -> float:
        ...

    @abstractmethod
    def obwod(self) -> float:
        ...


# Property — getter/setter
class Okrag:
    def __init__(self, promien: float) -> None:
        self._promien = promien

    @property
    def promien(self) -> float:
        return self._promien

    @promien.setter
    def promien(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Promień musi być dodatni")
        self._promien = value

o = Okrag(5.0)
o.promien = 10.0  # używa settera
print(o.promien)  # używa gettera
```

---

## Pętle

```python
# for
for i in range(10):
    print(i)

# for z indeksem
for i, value in enumerate(["a", "b", "c"]):
    print(i, value)  # 0 a, 1 b, 2 c

# for po słowniku
slownik = {"a": 1, "b": 2}
for key, value in slownik.items():
    print(key, value)

# while
i = 0
while i < 10:
    i += 1

# break i continue
for i in range(10):
    if i == 5:
        break       # przerywa pętlę
    if i % 2 == 0:
        continue    # przeskakuje do następnej iteracji

# List comprehension — tworzenie list w jednej linii
kwadraty = [x ** 2 for x in range(10)]
parzyste = [x for x in range(10) if x % 2 == 0]

# Dict comprehension
slownik = {k: v ** 2 for k, v in {"a": 1, "b": 2}.items()}

# Generator — leniwe obliczanie (oszczędza pamięć)
gen = (x ** 2 for x in range(1000000))  # nie liczy od razu
next(gen)  # liczy następny element
```

---

## Wyjątki

```python
# Rzucanie wyjątku
raise ValueError("Niepoprawna wartość")
raise TypeError("Niepoprawny typ")
raise RuntimeError("Coś poszło nie tak")

# Łapanie wyjątku
try:
    wynik = int(input("Podaj liczbę: "))
except ValueError:
    print("To nie jest liczba!")
except (TypeError, RuntimeError) as e:
    print(f"Błąd: {e}")
else:
    print("Sukces!")       # wykonuje się gdy nie ma wyjątku
finally:
    print("Zawsze się wykonuje")

# Własny wyjątek
class NiedodatniaPodstawaError(ValueError):
    pass

raise NiedodatniaPodstawaError("Podstawa musi być dodatnia")
```

---

## Stringi

```python
# f-string
imie = "Jan"
print(f"Cześć, {imie}!")
print(f"2 + 2 = {2 + 2}")
print(f"{3.14159:.2f}")      # zaokrąglenie do 2 miejsc: 3.14
print(f"{1000000:,}")        # separator tysięcy: 1,000,000
print(f"{'lewo':<10}")       # wyrównanie do lewej
print(f"{'prawo':>10}")      # wyrównanie do prawej

# Przydatne metody
"  hello  ".strip()          # "hello" — usuwa białe znaki
"hello world".split(" ")     # ["hello", "world"]
", ".join(["a", "b", "c"])   # "a, b, c"
"hello".upper()              # "HELLO"
"HELLO".lower()              # "hello"
"hello".replace("l", "r")   # "herro"
"hello".startswith("he")     # True
"hello".endswith("lo")       # True
"hello world".count("l")     # 3
```

---

## Listy i Słowniki — przydatne tricki

```python
# Unpacking
a, b, c = [1, 2, 3]
pierwsza, *reszta = [1, 2, 3, 4, 5]  # pierwsza=1, reszta=[2,3,4,5]

# Sortowanie
lista = [3, 1, 2]
lista.sort()                          # sortuje in-place
posortowana = sorted(lista)           # zwraca nową listę
osoby = [{"imie": "Jan", "wiek": 25}]
osoby.sort(key=lambda x: x["wiek"])  # sortowanie po kluczu

# Słownik — get z domyślną wartością
d = {"a": 1}
d.get("b", 0)    # 0 zamiast KeyError

# Merge słowników (Python 3.9+)
d1 = {"a": 1}
d2 = {"b": 2}
d3 = d1 | d2    # {"a": 1, "b": 2}

# Sprawdzenie czy klucz istnieje
"a" in d1       # True

# defaultdict — automatyczna domyślna wartość
from collections import defaultdict
d = defaultdict(list)
d["klucz"].append(1)  # nie rzuca KeyError
```

---

## Context Manager (with)

```python
# Pliki — automatycznie zamyka plik
with open("plik.txt", "r") as f:
    zawartosc = f.read()

# Zapis do pliku
with open("plik.txt", "w") as f:
    f.write("Hello, World!")
```

---

## Przydatne tricki

```python
# Walrus operator — przypisanie w warunku (Python 3.8+)
while chunk := f.read(1024):
    process(chunk)

# Ternary operator
x = "parzysta" if liczba % 2 == 0 else "nieparzysta"

# Zip — iterowanie po kilku listach naraz
for a, b in zip([1, 2, 3], ["a", "b", "c"]):
    print(a, b)  # 1 a, 2 b, 3 c

# Map i filter
kwadraty = list(map(lambda x: x ** 2, [1, 2, 3]))
parzyste = list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4]))

# any i all
any([False, True, False])   # True — czy choć jeden jest True
all([True, True, True])     # True — czy wszystkie są True

# enumerate z własnym startem
for i, v in enumerate(["a", "b", "c"], start=1):
    print(i, v)  # 1 a, 2 b, 3 c

# Odwracanie listy
lista = [1, 2, 3]
lista[::-1]         # [3, 2, 1]
list(reversed(lista))

# Spłaszczanie listy
zagniezdzona = [[1, 2], [3, 4], [5, 6]]
splaszczona = [x for podlista in zagniezdzona for x in podlista]

# _ jako zmienna do zignorowania
for _ in range(5):
    print("hello")

_, wazna_wartosc, _ = (1, 2, 3)
```

---

## Własne typy

```python
# TypeAlias — prosty alias na istniejący typ
from typing import TypeAlias

Wspolrzedna: TypeAlias = float
Punkt: TypeAlias = tuple[float, float]

def odleglosc(a: Punkt, b: Punkt) -> Wspolrzedna:
    ...


# NewType — nowy typ który nie miesza się z oryginałem
from typing import NewType

UserId = NewType("UserId", int)
PostId = NewType("PostId", int)

def pobierz_usera(user_id: UserId) -> str:
    ...

user_id = UserId(1)
post_id = PostId(1)

pobierz_usera(user_id)   # OK
pobierz_usera(post_id)   # mypy krzyknie! — to PostId nie UserId
pobierz_usera(1)         # mypy krzyknie! — to zwykły int


# TypedDict — słownik z określonymi kluczami i typami
from typing import TypedDict

class User(TypedDict):
    imie: str
    wiek: int
    admin: bool

user: User = {"imie": "Jan", "wiek": 25, "admin": False}  # OK
user: User = {"imie": "Jan"}  # mypy krzyknie! — brakuje kluczy


# Protocol — definiuje interfejs (jak interface w Javie)
from typing import Protocol

class Obliczalny(Protocol):
    def pole(self) -> float:
        ...

class Trojkat:
    def pole(self) -> float:
        return 7.5

def wypisz_pole(figura: Obliczalny) -> None:
    print(figura.pole())

wypisz_pole(Trojkat())  # OK
```

---

## Enum

```python
from enum import Enum, auto

class Kolor(Enum):
    CZERWONY = 1
    ZIELONY = 2
    NIEBIESKI = 3

# auto() — automatyczne wartości
class Kierunek(Enum):
    POLNOC = auto()
    POLUDNIE = auto()
    WSCHOD = auto()
    ZACHOD = auto()

# Użycie
kolor = Kolor.CZERWONY
print(kolor)        # Kolor.CZERWONY
print(kolor.value)  # 1
print(kolor.name)   # CZERWONY

# Porównywanie
kolor == Kolor.CZERWONY   # True
kolor == Kolor.ZIELONY    # False

# Iterowanie
for k in Kolor:
    print(k)

# Enum jako typ
def pomaluj(kolor: Kolor) -> None:
    ...

pomaluj(Kolor.CZERWONY)  # OK
pomaluj("czerwony")      # mypy krzyknie!
```

---

## Datetime

```python
from datetime import datetime, date, timedelta

# Teraz
teraz = datetime.now()
dzis = date.today()

# Tworzenie daty
data = datetime(2024, 1, 15, 12, 30, 0)
print(data.year)    # 2024
print(data.month)   # 1
print(data.day)     # 15

# Formatowanie
data.strftime("%Y-%m-%d")           # "2024-01-15"
data.strftime("%d.%m.%Y %H:%M")    # "15.01.2024 12:30"

# Parsowanie stringa
datetime.strptime("2024-01-15", "%Y-%m-%d")

# Operacje na datach
jutro = dzis + timedelta(days=1)
tydzien_temu = dzis - timedelta(weeks=1)
roznica = datetime(2024, 12, 31) - datetime.now()
print(roznica.days)  # ile dni do końca roku

# Type hint
def czy_minelo(data: datetime) -> bool:
    return data < datetime.now()
```

---

## Pathlib

```python
from pathlib import Path

# Tworzenie ścieżki
p = Path("folder/plik.txt")
p = Path.home() / "Documents" / "plik.txt"  # operator / zamiast os.path.join

# Informacje o ścieżce
p.name        # "plik.txt"
p.stem        # "plik"
p.suffix      # ".txt"
p.parent      # Path("folder")

# Sprawdzanie
p.exists()    # czy istnieje
p.is_file()   # czy to plik
p.is_dir()    # czy to folder

# Operacje na plikach
p.read_text()                    # czyta plik jako string
p.write_text("hello")           # zapisuje string do pliku
p.read_bytes()                   # czyta plik jako bytes

# Tworzenie folderów
Path("nowy/folder").mkdir(parents=True, exist_ok=True)

# Listowanie plików
for plik in Path(".").iterdir():
    print(plik)

# Glob — szukanie plików
for plik in Path(".").glob("**/*.py"):  # wszystkie .py rekurencyjnie
    print(plik)

# Type hint
def wczytaj_plik(sciezka: Path) -> str:
    return sciezka.read_text()
```

---

## Async / Await

```python
import asyncio

# Podstawowa funkcja async
async def pobierz_dane(url: str) -> str:
    await asyncio.sleep(1)  # symulacja czekania na odpowiedź
    return f"dane z {url}"

# Uruchomienie
asyncio.run(pobierz_dane("https://example.com"))

# Kilka zadań naraz — główna zaleta async
async def main() -> None:
    # BEZ asyncio.gather — wykonuje się po kolei (2 sekundy)
    wynik1 = await pobierz_dane("url1")
    wynik2 = await pobierz_dane("url2")

    # Z asyncio.gather — wykonuje się równolegle (1 sekunda)
    wynik1, wynik2 = await asyncio.gather(
        pobierz_dane("url1"),
        pobierz_dane("url2"),
    )

asyncio.run(main())

# Async context manager
async def zapisz() -> None:
    async with open("plik.txt", "w") as f:
        await f.write("hello")

# Async generator
async def generuj_liczby() -> None:
    for i in range(10):
        await asyncio.sleep(0.1)
        yield i

async def main() -> None:
    async for liczba in generuj_liczby():
        print(liczba)
```

---

## Generics

```python
from typing import TypeVar, Generic

T = TypeVar("T")

# Generyczna funkcja — działa dla dowolnego typu
def pierwszy(lista: list[T]) -> T:
    return lista[0]

pierwszy([1, 2, 3])        # zwraca int
pierwszy(["a", "b", "c"])  # zwraca str

# Generyczna klasa
class Stos(Generic[T]):
    def __init__(self) -> None:
        self._elementy: list[T] = []

    def push(self, element: T) -> None:
        self._elementy.append(element)

    def pop(self) -> T:
        return self._elementy.pop()

    def is_empty(self) -> bool:
        return len(self._elementy) == 0

stos_int = Stos[int]()
stos_int.push(1)
stos_int.push(2)
stos_int.pop()   # zwraca int

stos_str = Stos[str]()
stos_str.push("a")
stos_str.pop()   # zwraca str

# TypeVar z ograniczeniem — tylko konkretne typy
Liczba = TypeVar("Liczba", int, float)

def dodaj(a: Liczba, b: Liczba) -> Liczba:
    return a + b

dodaj(1, 2)        # OK — int
dodaj(1.0, 2.0)    # OK — float
dodaj("a", "b")    # mypy krzyknie!
```

---

## Moduły i importy

```python
# Import całego modułu
import math
math.sqrt(16)

# Import konkretnej funkcji
from math import sqrt, pi
sqrt(16)

# Import z aliasem
import numpy as np
from datetime import datetime as dt

# Import wszystkiego (unikaj!)
from math import *
```
