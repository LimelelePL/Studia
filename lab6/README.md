# lab6

---

## Requirements

- [uv](https://docs.astral.sh/uv/)

---

## Run

Install dependencies:
```bash
uv sync
```

Run the script:
```bash
uv run lab6
```

---

## Leniwe ładowanie danych (`Measurements`)

Klasa `Measurements` wczytuje dane z plików CSV w trzech etapach, odkładając każdy z nich do momentu gdy jest faktycznie potrzebny.

### Etap 1 — `__init__`: tylko skanowanie katalogu

Konstruktor jedynie listuje pliki CSV w podanym katalogu. Żaden plik nie jest otwierany.

```
Measurements("resources/measurements/")
    └─ glob("*.csv") → lista ścieżek
```

### Etap 2 — `_ensure_index`: czytanie nagłówków

Wywoływany przy pierwszym użyciu `__len__`, `__contains__`, `get_by_parameter` lub `get_by_station`. Otwiera każdy plik i czyta tylko wiersze nagłówka (do wiersza `Kod stanowiska` włącznie), by poznać dostępne stacje i wskaźniki. Wynik jest przechowywany w `_index` jako lista obiektów `SeriesEntry`. Kolejne wywołania `_ensure_index` są pomijane — indeks budowany jest tylko raz.

```
pierwsze get_by_parameter("C6H6")
    └─ _ensure_index()
        └─ dla każdego pliku: odczyt 6 wierszy nagłówka → SeriesEntry
```

### Etap 3 — `_load_file`: czytanie wierszy danych

Wywoływany dopiero gdy konkretna seria jest rzeczywiście potrzebna. Otwiera jeden plik CSV, pomija nagłówek i wczytuje wszystkie wiersze danych, tworząc obiekty `TimeSeries` dla każdej stacji z tego pliku. Gotowe serie trafiają do słownika `_cache`. Każdy plik ładowany jest co najwyżej raz.

```
get_by_parameter("C6H6")
    └─ _load_file("2023_C6H6_1g.csv")   ← tylko ten plik, nie pozostałe
        └─ odczyt wierszy danych → TimeSeries dla każdej stacji
```

### Wymuszenie pełnego załadowania

Metoda `detect_all_anomalies(validators, preload=True)` wymusza załadowanie wszystkich plików przed walidacją. Przy `preload=False` walidowane są tylko serie, które zostały już wcześniej załadowane.

```
detect_all_anomalies([...], preload=True)
    └─ _load_file(plik1), _load_file(plik2), ...   ← wszystkie pliki
detect_all_anomalies([...], preload=False)
    └─ waliduje tylko to co już jest w _cache
```
