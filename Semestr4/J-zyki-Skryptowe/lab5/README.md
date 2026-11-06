# lab5

---

## Requirements

- [uv](https://docs.astral.sh/uv/)

---

## Setup

Install dependencies:
```bash
uv sync
```

---

## CLI — argparse (`lab5`)

### Struktura wywołania

```
uv run lab5 --sensor <WSKAŹNIK> --frequency <CZĘSTOTLIWOŚĆ> --start <RRRR-MM-DD> --end <RRRR-MM-DD> <PODKOMENDA>
```

### Podkomenda `random` — losowa stacja

```bash
# Losowa stacja mierząca PM10 co godzinę w styczniu 2023
uv run lab5 --sensor PM10 --frequency 1g --start 2023-01-01 --end 2023-01-31 random

# Losowa stacja mierząca PM2.5 w całym roku
uv run lab5 --sensor PM25 --frequency 24g --start 2023-01-01 --end 2023-12-31 random

# Losowa stacja mierząca NO2 w sezonie letnim
uv run lab5 --sensor NO2 --frequency 1g --start 2023-06-01 --end 2023-08-31 random

# Losowa stacja mierząca SO2 w grudniu
uv run lab5 --sensor SO2 --frequency 24g --start 2023-12-01 --end 2023-12-31 random

# Losowa stacja mierząca benzen (C6H6) w lutym
uv run lab5 --sensor C6H6 --frequency 1g --start 2023-02-01 --end 2023-02-28 random

# Losowa stacja mierząca ozon w lipcu
uv run lab5 --sensor O3 --frequency 1g --start 2023-07-01 --end 2023-07-31 random

# Losowa stacja mierząca tlenek węgla
uv run lab5 --sensor CO --frequency 1g --start 2023-03-01 --end 2023-03-31 random

# Losowa stacja — pomiary dobowe PM10
uv run lab5 --sensor PM10 --frequency 24g --start 2023-06-01 --end 2023-08-31 random
# Przykładowy output:
# kod stacji: DsOlesBrzozo
# nazwa stacji: Oleśnica, ul. Brzozowa
# miejscowosc: Oleśnica
# adres: ul. Brzozowa 7
```

### Podkomenda `stats` — statystyki dla stacji

```bash
# Statystyki PM10 dla stacji przy Bulwarze w Krakowie — styczeń 2023
uv run lab5 --sensor PM10 --frequency 1g --start 2023-01-01 --end 2023-01-31 stats MpKrakBulwar
# kod stacji: MpKrakBulwar
# liczba pomiarow: 706
# srednia: 25.9699
# odchylenie standardowe: 16.4847

# Statystyki PM10 dla stacji w Warszawie — cały rok
uv run lab5 --sensor PM10 --frequency 1g --start 2023-01-01 --end 2023-12-31 stats MzWarAlNiepo

# Statystyki NO2 dla stacji w Krakowie — kwartał zimowy
uv run lab5 --sensor NO2 --frequency 1g --start 2023-01-01 --end 2023-03-31 stats MpKrakAlKras

# Statystyki PM2.5 dobowe — stacja we Wrocławiu
uv run lab5 --sensor PM25 --frequency 24g --start 2023-10-01 --end 2023-12-31 stats DsWrocWybCon

# Statystyki SO2 — stacja w Katowicach przez cały rok
uv run lab5 --sensor SO2 --frequency 1g --start 2023-01-01 --end 2023-12-31 stats SlKatoKossut

# Statystyki ozonu latem w Krakowie
uv run lab5 --sensor O3 --frequency 1g --start 2023-06-01 --end 2023-08-31 stats MpKrakOsPias

# Statystyki benzenu — stacja w Gdańsku
uv run lab5 --sensor C6H6 --frequency 1g --start 2023-01-01 --end 2023-06-30 stats PmGdaWyzwole

# Statystyki PM10 dobowe — Łódź jesień
uv run lab5 --sensor PM10 --frequency 24g --start 2023-09-01 --end 2023-11-30 stats LdLodzGdansk
```

### Błędne wywołania — walidacja

```bash
# Błędny format daty
uv run lab5 --sensor PM10 --frequency 1g --start 01-01-2023 --end 31-01-2023 random
# error: Nieprawidlowy format daty

# Data końcowa wcześniejsza niż początkowa
uv run lab5 --sensor PM10 --frequency 1g --start 2023-12-31 --end 2023-01-01 random
# error: niepoprawny zakres dat

# Nieistniejący wskaźnik
uv run lab5 --sensor XYZ --frequency 1g --start 2023-01-01 --end 2023-01-31 random
# error: argument --sensor: invalid choice

# Nieistniejąca stacja (podkomenda stats)
uv run lab5 --sensor PM10 --frequency 1g --start 2023-01-01 --end 2023-01-31 stats NIEISTNIEJACA
# WARNING: Stacja 'NIEISTNIEJACA' nie wspiera podanego wskaźnika lub nie ma pomiarów
```

---

## CLI — typer (`lab5-typer`)

### Struktura wywołania

```
uv run lab5-typer --sensor <WSKAŹNIK> --frequency <CZĘSTOTLIWOŚĆ> --start <RRRR-MM-DD> --end <RRRR-MM-DD> <PODKOMENDA>
```

### Help

```bash
# Główna pomoc
uv run lab5-typer --help

# Pomoc dla podkomendy random
uv run lab5-typer --sensor PM10 --frequency 1g --start 2023-01-01 --end 2023-01-31 random --help

# Pomoc dla podkomendy stats
uv run lab5-typer --sensor PM10 --frequency 1g --start 2023-01-01 --end 2023-01-31 stats --help
```

### Podkomenda `random` — losowa stacja

```bash
# Losowa stacja mierząca PM10 w zimie
uv run lab5-typer --sensor PM10 --frequency 1g --start 2023-12-01 --end 2023-12-31 random

# Losowa stacja mierząca NO2 — cały rok
uv run lab5-typer --sensor NO2 --frequency 1g --start 2023-01-01 --end 2023-12-31 random

# Losowa stacja — pomiary dobowe PM2.5
uv run lab5-typer --sensor PM25 --frequency 24g --start 2023-04-01 --end 2023-06-30 random

# Losowa stacja mierząca ozon w sezonie letnim
uv run lab5-typer --sensor O3 --frequency 1g --start 2023-05-01 --end 2023-09-30 random

# Losowa stacja mierząca tlenek azotu
uv run lab5-typer --sensor NO --frequency 1g --start 2023-01-01 --end 2023-03-31 random

# Losowa stacja mierząca rtęć
uv run lab5-typer --sensor "Hg(TGM)" --frequency 1g --start 2023-01-01 --end 2023-12-31 random

# Losowa stacja — pomiary dobowe SO2
uv run lab5-typer --sensor SO2 --frequency 24g --start 2023-11-01 --end 2023-11-30 random
```

### Podkomenda `stats` — statystyki dla stacji

```bash
# Statystyki PM10 — Kraków Bulwar, styczeń 2023
uv run lab5-typer --sensor PM10 --frequency 1g --start 2023-01-01 --end 2023-01-31 stats MpKrakBulwar
# kod stacji: MpKrakBulwar
# liczba pomiarow: 706
# srednia: 25.9699
# odchylenie standardowe: 16.4847

# Statystyki NO2 — Kraków al. Krasińskiego, wiosna
uv run lab5-typer --sensor NO2 --frequency 1g --start 2023-03-01 --end 2023-05-31 stats MpKrakAlKras

# Statystyki PM2.5 dobowe — Wrocław, cały rok
uv run lab5-typer --sensor PM25 --frequency 24g --start 2023-01-01 --end 2023-12-31 stats DsWrocWybCon

# Statystyki SO2 — Katowice, zima
uv run lab5-typer --sensor SO2 --frequency 1g --start 2023-01-01 --end 2023-02-28 stats SlKatoKossut

# Statystyki O3 — Warszawa, lato
uv run lab5-typer --sensor O3 --frequency 1g --start 2023-06-01 --end 2023-08-31 stats MzWarAlNiepo

# Statystyki CO — Gdańsk, luty
uv run lab5-typer --sensor CO --frequency 1g --start 2023-02-01 --end 2023-02-28 stats PmGdaLeczkow

# Statystyki PM10 dobowe — Łódź, jesień
uv run lab5-typer --sensor PM10 --frequency 24g --start 2023-09-01 --end 2023-11-30 stats LdLodzGdansk

# Statystyki NOx — Bydgoszcz, kwiecień
uv run lab5-typer --sensor NOx --frequency 1g --start 2023-04-01 --end 2023-04-30 stats KpBydWarszaw
```

### Błędne wywołania — walidacja

```bash
# Nieznany wskaźnik — lista dostępnych wyświetlana automatycznie
uv run lab5-typer --sensor XYZ --frequency 1g --start 2023-01-01 --end 2023-01-31 random
# Error: Invalid value for --sensor: Nieznany wskaźnik. Dostępne: As(PM10), BaA(PM10), ...

# Nieznana częstotliwość
uv run lab5-typer --sensor PM10 --frequency 2g --start 2023-01-01 --end 2023-01-31 random
# Error: Invalid value for --frequency: Nieznana częstotliwość. Dostępne: 1g, 24g

# Błędny format daty
uv run lab5-typer --sensor PM10 --frequency 1g --start 01/01/2023 --end 31/01/2023 random
# Error: Invalid value for --start: Nieprawidłowy format: '01/01/2023'. Użyj RRRR-MM-DD.

# Data końcowa wcześniejsza niż początkowa
uv run lab5-typer --sensor PM10 --frequency 1g --start 2023-12-31 --end 2023-01-01 random
# Error: Invalid value for --start / --end: Data początkowa musi być wcześniejsza lub równa końcowej.
```

---

## Testy

```bash
# Wszystkie testy
uv run pytest

# Z podglądem każdego testu
uv run pytest -v

# Tylko jeden moduł
uv run pytest tests/test_parser.py -v
uv run pytest tests/test_cli.py -v
uv run pytest tests/test_stations_tasks.py -v

# Tylko failujące
uv run pytest --lf

# Z logami (przydatne przy debugowaniu)
uv run pytest -s
```
