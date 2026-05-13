from datetime import datetime
from pathlib import Path

from app.detectors import OutlierDetector, ThresholdDetector, ZeroSpikeDetector
from app.measurements import Measurements

from app.detectors import OutlierDetector, SimpleReporter, ThresholdDetector, ZeroSpikeDetector
from app.measurements import Measurements
from app.timeseries import TimeSeries

def demo_measurements() -> None:
    measurements_path = Path(__file__).resolve().parents[2] / "resources" / "measurements"
    measurements = Measurements(measurements_path)

    print(f"Liczba serii w indeksie: {len(measurements)}")
    print(f"Czy parametr 'As(PM10)' istnieje: {'As(PM10)' in measurements}")

    parameter_series = measurements.get_by_parameter("As(PM10)")
    print(f"Liczba serii dla 'As(PM10)': {len(parameter_series)}")

    if parameter_series:
        first_series = parameter_series[0]
        print(
            "Przykladowa seria po parametrze:",
            first_series.code,
            first_series.sensor,
            first_series.averaging_time,
            first_series.unit,
        )

        station_series = measurements.get_by_station(first_series.code)
        print(f"Liczba serii dla stacji '{first_series.code}': {len(station_series)}")

    validators = [
        OutlierDetector(k=2.0),
        ZeroSpikeDetector(),
        ThresholdDetector(threshold=0.05),
    ]

    anomalies = measurements.detect_all_anomalies(validators, preload=True)
    print("\nPrzykladowe wyniki detektorow:")

    printed = 0
    for series_name, messages in anomalies.items():
        if not messages:
            continue

        print(f"\n{series_name}:")
        for message in messages:
            print(f" - {message}")

        printed += 1
        if printed == 3:
            break

    if printed == 0:
        print("Brak wykrytych anomalii.")


def demo_detect_anomalies() -> None:
    measurements_dir = Path(__file__).parent.parent.parent / "resources" / "measurements"
    m = Measurements(measurements_dir)

    validators = [
        OutlierDetector(k=2.0),
        ZeroSpikeDetector(),
        ThresholdDetector(threshold=50.0),
    ]

    m.get_by_parameter("C6H6")  # załaduj C6H6 przed detekcją

    wyniki = m.detect_all_anomalies(validators, preload=False)

    print("\n[detect_all_anomalies — serie C6H6]")
    for klucz, komunikaty in wyniki.items():
        if komunikaty:
            print(f"\n  {klucz}:")
            for msg in komunikaty:
                print(f"    {msg}")


def main() -> None:
    demo_duck_typing()
    demo_detect_anomalies()


if __name__ == "__main__":
    main()
