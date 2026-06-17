import argparse
import csv
from pathlib import Path

from sqlalchemy import create_engine, insert
from sqlalchemy.orm import Session

from app.orm.db_structure import Calendar, Route, Stop, StopTime, Trip

TABLE_MODELS = {
    "stops": Stop,
    "routes": Route,
    "calendar": Calendar,
    "trips": Trip,
    "stop_times": StopTime,
}


def get_args() -> tuple[str, str]:
    parser = argparse.ArgumentParser()
    parser.add_argument("db_path", type=str)
    parser.add_argument("dir_path", type=str)

    args = parser.parse_args()
    return args.db_path, args.dir_path


def collect_files(dir_path: Path) -> list[Path]:
    files_to_load = ["stops.txt", "routes.txt", "calendar.txt", "trips.txt", "stop_times.txt"]
    file_paths = [dir_path / file_name for file_name in files_to_load]

    missing_files = [file_path.name for file_path in file_paths if not file_path.exists()]
    if missing_files:
        raise FileNotFoundError(f"Brak plikow do ladowania danych: {', '.join(missing_files)}")

    return file_paths


def insert_file_into_db(session: Session, file_path: Path, table_name: str, batch_size: int = 1000) -> None:
    model = TABLE_MODELS[table_name]

    with open(file_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"Plik {file_path} nie ma naglowka")

        batch = []
        for row in reader:
            batch.append(dict(row))

            if len(batch) == batch_size:
                session.execute(insert(model), batch)
                batch.clear()

        if batch:
            session.execute(insert(model), batch)


def load_data(db_path: Path, dir_path: Path) -> None:
    if not db_path.exists() or not dir_path.is_dir():
        raise FileNotFoundError("plik bazy danych lub katalog z danymi nie istnieje")

    engine = create_engine(f"sqlite:///{db_path}")
    load_file_paths = collect_files(dir_path)

    with Session(engine) as session:
        for file_path in load_file_paths:
            insert_file_into_db(session, file_path, file_path.stem.strip())
        session.commit()


if __name__ == "__main__":
    db_path_arg, dir_path_arg = get_args()
    load_data(Path(db_path_arg), Path(dir_path_arg))
