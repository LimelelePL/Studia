from datetime import datetime

import numpy as np

from app.detectors import OutlierDetector, SimpleReporter, ThresholdDetector, ZeroSpikeDetector
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


def main() -> None:
    demo_duck_typing()


if __name__ == "__main__":
    main()
