from datetime import datetime
from typing import Annotated

import typer

from app.cli import (
    get_all_measurements_in_range,
    get_filtered_pathes,
    possible_unit_measurements,
    print_random_station,
    print_stats,
    setup_logging,
)
from app.constants import MEASUREMENTS_PATH

app = typer.Typer(help="Analiza danych ze stacji pomiarowych.")


def _parse_date(value: str, param_hint: str) -> datetime:
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise typer.BadParameter(
            f"Nieprawidłowy format: '{value}'. Użyj RRRR-MM-DD.",
            param_hint=param_hint,
        )


@app.callback()
def main(
    ctx: typer.Context,
    sensor: Annotated[str, typer.Option(help="Mierzona wielkość (PM10, PM2.5, ...)")],
    frequency: Annotated[str, typer.Option(help="Częstotliwość pomiaru (1g, 24g)")],
    start: Annotated[str, typer.Option(help="Data początkowa RRRR-MM-DD")],
    end: Annotated[str, typer.Option(help="Data końcowa RRRR-MM-DD")],
) -> None:
    setup_logging()
    measurements, frequencies = possible_unit_measurements(MEASUREMENTS_PATH)

    if sensor not in measurements:
        raise typer.BadParameter(
            f"Nieznany wskaźnik. Dostępne: {', '.join(sorted(measurements))}",
            param_hint="--sensor",
        )

    if frequency not in frequencies:
        raise typer.BadParameter(
            f"Nieznana częstotliwość. Dostępne: {', '.join(sorted(frequencies))}",
            param_hint="--frequency",
        )

    start_dt = _parse_date(start, "--start")
    end_dt = _parse_date(end, "--end")

    if start_dt > end_dt:
        raise typer.BadParameter(
            "Data początkowa musi być wcześniejsza lub równa końcowej.",
            param_hint="--start / --end",
        )

    ctx.ensure_object(dict)
    ctx.obj["sensor"] = sensor
    ctx.obj["frequency"] = frequency
    ctx.obj["start"] = start_dt
    ctx.obj["end"] = end_dt


@app.command()
def random(ctx: typer.Context) -> None:
    """Wypisuje nazwę i adres losowej stacji mierzącej daną wielkość."""
    try:
        filtered = get_filtered_pathes(ctx.obj["sensor"], ctx.obj["frequency"])
        if not filtered:
            raise SystemExit(1)
        records = get_all_measurements_in_range(filtered, ctx.obj["start"], ctx.obj["end"])
        if not records:
            raise SystemExit(1)
        print_random_station(records)
    except FileNotFoundError:
        raise SystemExit(1)


@app.command()
def stats(
    ctx: typer.Context,
    station_code: Annotated[str, typer.Argument(help="Kod stacji")],
) -> None:
    """Oblicza średnią i odchylenie standardowe dla danej stacji."""
    try:
        filtered = get_filtered_pathes(ctx.obj["sensor"], ctx.obj["frequency"])
        if not filtered:
            raise SystemExit(1)
        records = get_all_measurements_in_range(filtered, ctx.obj["start"], ctx.obj["end"])
        if not records:
            raise SystemExit(1)
        print_stats(records, station_code)
    except FileNotFoundError:
        raise SystemExit(1)


if __name__ == "__main__":
    app()
