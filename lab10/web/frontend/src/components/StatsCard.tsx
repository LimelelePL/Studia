import { Card } from "@heroui/react";

import type { Stats } from "../types";

interface Props {
  stats: Stats;
}

export function StatsCard({ stats }: Props) {
  return (
    <Card className="bg-[#f8fafd] p-4">
      <Card.Content className="flex flex-col gap-4">
        <h2 className="text-xl font-bold">{stats.stop.stop_name}</h2>

        <div className="grid grid-cols-2 gap-1 text-sm">
          <span>Różnych linii:</span>
          <span className="font-semibold">{stats.count_routes}</span>
          <span>Liczba odjazdów:</span>
          <span className="font-semibold">{stats.count_departures}</span>
          <span>Najwcześniejszy odjazd:</span>
          <span className="font-semibold">{stats.first_departure ?? "—"}</span>
          <span>Najpóźniejszy odjazd:</span>
          <span className="font-semibold">{stats.last_departure ?? "—"}</span>
        </div>

        <div>
          <h3 className="font-semibold">Najczęstsze kierunki</h3>
          <ul className="list-disc pl-5 text-sm">
            {stats.directions.map((d, i) => (
              <li key={i}>
                {d.direction ?? "—"}: {d.count}
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h3 className="font-semibold">Linie i kierunki (z zakresem godzin)</h3>
          <ul className="list-disc pl-5 text-sm">
            {stats.by_route.map((r, i) => (
              <li key={i}>
                linia {r.route} → {r.direction ?? "—"}: {r.count} odjazdów (od {r.first} do {r.last})
              </li>
            ))}
          </ul>
        </div>
      </Card.Content>
    </Card>
  );
}
