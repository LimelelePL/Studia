import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, distinct, func, select
from sqlalchemy.orm import sessionmaker

from app.orm.db_structure import Route, Stop, StopTime, Trip

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = Path(os.environ.get("LAB10_DB", PROJECT_ROOT / "database" / "my_timetable.sqlite3"))

engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(bind=engine)

app = FastAPI(title="lab10 — Rozkład jazdy API")

# Vite proxy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/stops")
def search_stops(q: str = "") -> list[dict]:
    """Zwraca do 20 przystanków pasujących do fragmentu nazwy."""
    with SessionLocal() as session:
        rows = session.execute(
            select(Stop.stop_id, Stop.stop_code, Stop.stop_name)
            .where(Stop.stop_name.like(f"%{q}%"))
            .order_by(Stop.stop_name, Stop.stop_code)
            .limit(20)
        ).all()

    return [{"stop_id": r.stop_id, "stop_code": r.stop_code, "stop_name": r.stop_name} for r in rows]


@app.get("/api/stops/{stop_id}/stats")
def stop_stats(stop_id: int) -> dict:
    """Komplet statystyk dla wybranego przystanku."""
    with SessionLocal() as session:
        stop = session.get(Stop, stop_id)
        if stop is None:
            raise HTTPException(status_code=404, detail="Nie znaleziono przystanku")

        # a) liczba różnych linii
        count_routes = session.execute(
            select(func.count(distinct(Route.route_id)))
            .select_from(StopTime)
            .join(Trip, Trip.trip_id == StopTime.trip_id)
            .join(Route, Route.route_id == Trip.route_id)
            .where(StopTime.stop_id == stop_id)
        ).scalar_one()

        # b) liczba odjazdów
        count_departures = session.execute(
            select(func.count()).select_from(StopTime).where(StopTime.stop_id == stop_id)
        ).scalar_one()

        # c) najwcześniejszy i najpóźniejszy odjazd
        first_departure, last_departure = session.execute(
            select(func.min(StopTime.departure_time), func.max(StopTime.departure_time)).where(
                StopTime.stop_id == stop_id
            )
        ).one()

        # d) najczęstsze kierunki
        directions = session.execute(
            select(Trip.trip_headsign, func.count().label("cnt"))
            .select_from(StopTime)
            .join(Trip, Trip.trip_id == StopTime.trip_id)
            .where(StopTime.stop_id == stop_id)
            .group_by(Trip.trip_headsign)
            .order_by(func.count().desc(), Trip.trip_headsign)
            .limit(10)
        ).all()

        # e) własne, nietrywialne zapytanie — linie + kierunki + zakres godzin
        by_route = session.execute(
            select(
                Route.route_short_name,
                Trip.trip_headsign,
                func.count().label("cnt"),
                func.min(StopTime.departure_time),
                func.max(StopTime.departure_time),
            )
            .select_from(StopTime)
            .join(Trip, Trip.trip_id == StopTime.trip_id)
            .join(Route, Route.route_id == Trip.route_id)
            .where(StopTime.stop_id == stop_id)
            .group_by(Route.route_id, Route.route_short_name, Trip.trip_headsign)
            .order_by(func.count().desc(), Route.route_short_name, Trip.trip_headsign)
            .limit(10)
        ).all()

    return {
        "stop": {"stop_id": stop.stop_id, "stop_code": stop.stop_code, "stop_name": stop.stop_name},
        "count_routes": count_routes,
        "count_departures": count_departures,
        "first_departure": first_departure,
        "last_departure": last_departure,
        "directions": [{"direction": d[0], "count": d[1]} for d in directions],
        "by_route": [{"route": r[0], "direction": r[1], "count": r[2], "first": r[3], "last": r[4]} for r in by_route],
    }
