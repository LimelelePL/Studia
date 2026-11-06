from pathlib import Path

from app.detectors import OutlierDetector, ThresholdDetector, ZeroSpikeDetector
from app.measurements import Measurements


def run_demo() -> list[str]:
    measurements_path = Path(__file__).resolve().parents[2] / "resources" / "measurements"
    measurements = Measurements(measurements_path)
    measurements.get_by_parameter("C6H6")

    validators = [
        OutlierDetector(k=2.0),
        ZeroSpikeDetector(),
        ThresholdDetector(threshold=50.0),
    ]
    anomalies = measurements.detect_all_anomalies(validators, preload=False)

    messages: list[str] = []
    for series_name, series_messages in anomalies.items():
        messages.extend(f"{series_name}: {message}" for message in series_messages)
    return messages


def main() -> None:
    run_demo()


if __name__ == "__main__":
    main()
