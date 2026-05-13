from datetime import datetime
from pathlib import Path

import numpy as np

from app.detectors import OutlierDetector, SimpleReporter, ThresholdDetector, ZeroSpikeDetector
from app.measurements import Measurements
from app.timeseries import TimeSeries


def demo_duck_typing() -> None:

    timestamps = [datetime(2023, 1, 1, h) for h in range(1, 11)]
    values = np.array([1.0, 2.0, 0.0, 0.0, 0.0, 3.0, 100.0, 2.5, 1.5, 2.0])
    series = TimeSeries(
        sensor="C6H6",
        code="DsWrocWybCon",
        averaging_time="1g",
        timestamps=timestamps,
        values=values,
        unit="ug/m3",
    )

    analyzers = [
        OutlierDetector(k=2.0),
        ZeroSpikeDetector(),
        ThresholdDetector(threshold=50.0),
        SimpleReporter(),  # not a SeriesValidator subclass — duck typing!
    ]

    for analyzer in analyzers:
        results = analyzer.analyze(series)
        print(f"\n[{type(analyzer).__name__}]")
        if results:
            for msg in results:
                print(" ", msg)
        else:
            print("Brak anomalii.")


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
