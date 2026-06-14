import sqlite3
import sys
from pathlib import Path


def create_database(db_name: str, sql_file_path: Path) -> None:
    if not sql_file_path.exists() or sql_file_path.suffix != ".sql":
        raise FileNotFoundError("brak pliku zrodlowego .sql")

    project_dir = Path(__file__).resolve().parents[2]
    database_dir = project_dir / "database"
    database_dir.mkdir(exist_ok=True)

    db_path = database_dir / db_name
    if db_path.suffix == "":
        db_path = db_path.with_suffix(".sqlite3")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(sql_file_path) as f:
        sql_script = f.read()

    try:
        cursor.executescript(sql_script)
        conn.commit()
        print(f"Utworzono baze danych: {db_path}")
    except sqlite3.Error as e:
        print(f"Wystapil blad podczas importowania: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uzycie: python create_database.py nazwa_bazy")
        sys.exit(1)

    name = sys.argv[1]
    sql_path = Path(__file__).resolve().with_name("create_tables.sql")
    create_database(name, sql_path)
