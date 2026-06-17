# Interfejs webowy (zadanie 3)

Prosty interfejs do przeglądania statystyk przystanku:

- **backend** — FastAPI (`web/backend/api.py`), reużywa modeli SQLAlchemy ORM z `app.orm.db_structure`,
- **frontend** — React + Vite + [HeroUI](https://heroui.com) (`web/frontend/`).

## 1. Baza danych

Aplikacja webowa czyta z pliku `database/my_timetable.sqlite3` (zwykły plik SQLite —
nie ma osobnego serwera bazy). Backend potrzebuje, żeby ten plik **istniał i zawierał dane**.

**Plik z danymi jest już w repozytorium**, więc zwykle ten krok można pominąć — wystarczy
zainstalować zależności i przejść do punktu 2:

```bash
uv sync
```

Komendy poniżej są potrzebne **tylko gdy** plik bazy nie istnieje / jest pusty albo chcesz
zbudować go od nowa ze świeżej paczki GTFS (krok jednorazowy / odtworzeniowy):

```bash
uv run python -m app.orm.create_database my_timetable                                              # tworzy pustą strukturę
uv run python -m app.orm.load_data database/my_timetable.sqlite3 resources/OtwartyWroclaw_rozklad_jazdy  # wypełnia danymi
```

> Sprawdzenie, czy baza ma dane:
> `sqlite3 database/my_timetable.sqlite3 "SELECT COUNT(*) FROM stop_times"` (powinno być > 0).

## 2. Uruchom backend (terminal 1)

Z katalogu głównego projektu:

```bash
uv run uvicorn web.backend.api:app --reload --port 8000
```

API działa na <http://localhost:8000> (dokumentacja: <http://localhost:8000/docs>).
Inną bazę wskażesz zmienną `LAB10_DB`, np.:

```bash
LAB10_DB="$PWD/database/my_timetable.sqlite3" uv run uvicorn web.backend.api:app --port 8000
```

## 3. Uruchom frontend (terminal 2)

```bash
cd web/frontend
npm install
npm run dev
```

Otwórz adres wypisany przez Vite (domyślnie <http://localhost:5173>).
Vite przekierowuje zapytania `/api/*` do backendu na porcie 8000 (patrz `vite.config.ts`),
więc nie ma problemów z CORS.

## Endpointy API

| Metoda | Ścieżka | Opis |
|---|---|---|
| GET | `/api/stops?q=<fraza>` | do 20 przystanków pasujących do fragmentu nazwy |
| GET | `/api/stops/{stop_id}/stats` | komplet statystyk przystanku (zadanie 3 a–e) |
