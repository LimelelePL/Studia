import argparse
import csv
import sqlite3
from pathlib import Path


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


def insert_file_into_db(db_path: Path, file_path: Path, table_name: str, batch_size: int = 1000) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        with open(file_path, encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                raise ValueError(f"Plik {file_path} nie ma naglowka")

            columns = reader.fieldnames
            columns_sql = ", ".join(f'"{column}"' for column in columns)
            placeholders = ", ".join(["?"] * len(columns))
            query = f'INSERT INTO "{table_name}" ({columns_sql}) VALUES ({placeholders})'

            batch = []
            for row in reader:
                batch.append(tuple(row[column] for column in columns))

                if len(batch) == batch_size:
                    cursor.executemany(query, batch)
                    batch.clear()

            if batch:
                cursor.executemany(query, batch)

        conn.commit()


def load_data(db_path: Path, dir_path: Path):
    if not db_path.exists() or not dir_path.is_dir():
        raise FileNotFoundError("plik bazy danych lub katalog z danymi nie istnieje")

    load_file_paths = collect_files(dir_path)
    for file in load_file_paths:
        insert_file_into_db(db_path, file, file.stem.strip())


if __name__ == "__main__":
    db_path, dir_path = get_args()
    load_data(Path(db_path), Path(dir_path))
