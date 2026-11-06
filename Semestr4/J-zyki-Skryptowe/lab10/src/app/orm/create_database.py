import argparse
from pathlib import Path

from sqlalchemy import create_engine

from app.orm.db_structure import Base


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("db_name", type=str)
    return parser.parse_args()


def get_database_path(db_name: str) -> Path:
    project_dir = Path(__file__).resolve().parents[3]
    database_dir = project_dir / "database"
    database_dir.mkdir(exist_ok=True)

    db_path = database_dir / db_name
    if db_path.suffix == "":
        db_path = db_path.with_suffix(".sqlite3")

    return db_path


def create_database(db_name: str) -> Path:
    db_path = get_database_path(db_name)
    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)
    return db_path


def main() -> None:
    args = get_args()
    db_path = create_database(args.db_name)
    print(f"Utworzono baze danych ORM: {db_path}")


if __name__ == "__main__":
    main()
