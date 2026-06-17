import argparse
import sqlite3
from pathlib import Path
from typing import cast

from sqlalchemy import Engine, create_engine, distinct, func, select
from sqlalchemy.orm import Session

from app.orm.db_structure import Route, StopTime, Trip


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("db_path", type=Path)
    parser.add_argument("--stop-id", type=int)
    return parser.parse_args()


def connect_database(db_path: Path) -> tuple[sqlite3.Connection, Engine]:
    if not db_path.exists():
        raise FileNotFoundError(f"Nie znaleziono bazy danych: {db_path}")

    conn = sqlite3.connect(db_path)
    engine = create_engine(f"sqlite:///{db_path}")
    conn.row_factory = sqlite3.Row
    return conn, engine


def choose_stop(conn: sqlite3.Connection) -> int:
    phrase = input("Podaj fragment nazwy przystanku: ").strip()

    stops = conn.execute(
        """
        SELECT stop_id, stop_code, stop_name
        FROM stops
        WHERE stop_name LIKE ?
        ORDER BY stop_name, stop_code
        LIMIT 20
        """,
        (f"%{phrase}%",),
    ).fetchall()

    if not stops:
        raise ValueError("Nie znaleziono przystankow dla podanej frazy")

    for index, stop in enumerate(stops, start=1):
        print(f"{index}. {stop['stop_name']} | kod: {stop['stop_code']} | id: {stop['stop_id']}")

    choice = int(input("Wybierz numer przystanku z listy: "))
    if choice < 1 or choice > len(stops):
        raise ValueError("Niepoprawny numer przystanku")

    return int(stops[choice - 1]["stop_id"])


def get_stop(conn: sqlite3.Connection, stop_id: int) -> sqlite3.Row:
    stop = conn.execute(
        """
        SELECT stop_id, stop_code, stop_name
        FROM stops
        WHERE stop_id = ?
        """,
        (stop_id,),
    ).fetchone()

    if stop is None:
        raise ValueError(f"Nie znaleziono przystanku o id {stop_id}")

    return cast(sqlite3.Row, stop)


def count_routes(conn: sqlite3.Connection, stop_id: int) -> int:
    return int(
        conn.execute(
            """
            SELECT COUNT(DISTINCT routes.route_id)
            FROM stop_times
            JOIN trips ON trips.trip_id = stop_times.trip_id
            JOIN routes ON routes.route_id = trips.route_id
            WHERE stop_times.stop_id = ?
            """,
            (stop_id,),
        ).fetchone()[0],
    )

def count_routes_alchemy(session: Session, stop_id: int) -> int:
    result = session.execute(
        select(func.count(distinct(Route.route_id)))
        .select_from(StopTime)
        .join(Trip, Trip.trip_id == StopTime.trip_id)
        .join(Route, Route.route_id == Trip.route_id)
        .where(StopTime.stop_id == stop_id)
    ).scalar_one()

    return int(result)


def count_departures(conn: sqlite3.Connection, stop_id: int) -> int:
    return int(
        conn.execute(
            """
            SELECT COUNT(*)
            FROM stop_times
            WHERE stop_id = ?
            """,
            (stop_id,),
        ).fetchone()[0],
    )


def get_first_and_last_departure(conn: sqlite3.Connection, stop_id: int) -> sqlite3.Row:
    row = conn.execute(
        """
        SELECT MIN(departure_time) AS first_departure,
               MAX(departure_time) AS last_departure
        FROM stop_times
        WHERE stop_id = ?
        """,
        (stop_id,),
    ).fetchone()
    return cast(sqlite3.Row, row)


def get_most_common_directions(conn: sqlite3.Connection, stop_id: int) -> list[sqlite3.Row]:
    return conn.execute(
        """
        SELECT trips.trip_headsign AS direction,
               COUNT(*) AS departures_count
        FROM stop_times
        JOIN trips ON trips.trip_id = stop_times.trip_id
        WHERE stop_times.stop_id = ?
        GROUP BY trips.trip_headsign
        ORDER BY departures_count DESC, direction
        LIMIT 10
        """,
        (stop_id,),
    ).fetchall()


def get_departures_by_route(conn: sqlite3.Connection, stop_id: int) -> list[sqlite3.Row]:
    return conn.execute(
        """
        SELECT routes.route_short_name AS route,
               trips.trip_headsign AS direction,
               COUNT(*) AS departures_count,
               MIN(stop_times.departure_time) AS first_departure,
               MAX(stop_times.departure_time) AS last_departure
        FROM stop_times
        JOIN trips ON trips.trip_id = stop_times.trip_id
        JOIN routes ON routes.route_id = trips.route_id
        WHERE stop_times.stop_id = ?
        GROUP BY routes.route_id, routes.route_short_name, trips.trip_headsign
        ORDER BY departures_count DESC, routes.route_short_name, trips.trip_headsign
        LIMIT 10
        """,
        (stop_id,),
    ).fetchall()


def print_stop_stats(conn: sqlite3.Connection, session: Session, stop_id: int) -> None:
    stop = get_stop(conn, stop_id)
    departures = get_first_and_last_departure(conn, stop_id)

    print(f"\nPrzystanek: {stop['stop_name']} | kod: {stop['stop_code']} | id: {stop['stop_id']}")
    print(f"Liczba roznych linii: {count_routes_alchemy(session, stop_id)}")
    print(f"Liczba odjazdow: {count_departures(conn, stop_id)}")
    print(f"Najwczesniejszy odjazd: {departures['first_departure']}")
    print(f"Najpozniejszy odjazd: {departures['last_departure']}")

    print("\nNajczestsze kierunki:")
    for row in get_most_common_directions(conn, stop_id):
        print(f"- {row['direction']}: {row['departures_count']}")

    print("\nDodatkowe zapytanie - najczestsze linie i kierunki na przystanku:")
    for row in get_departures_by_route(conn, stop_id):
        print(
            f"- linia {row['route']} do {row['direction']}: "
            f"{row['departures_count']} odjazdow, "
            f"od {row['first_departure']} do {row['last_departure']}"
        )


def main() -> None:
    args = get_args()

    conn, engine = connect_database(args.db_path)
    with Session(engine) as session:
        stop_id = args.stop_id if args.stop_id is not None else choose_stop(conn)
        print_stop_stats(conn, session, stop_id)
        conn.close()


if __name__ == "__main__":
    main()
