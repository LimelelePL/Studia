import { Button } from "@heroui/react";

import type { Stop } from "../types";

interface Props {
  stops: Stop[];
  onSelect: (stopId: number) => void;
}

export function StopList({ stops, onSelect }: Props) {
  return (
    <div className="flex flex-col gap-1">
      <h2 className="font-semibold">Wybierz przystanek z listy:</h2>
      {stops.map((s) => (
        <Button
          key={s.stop_id}
          variant="ghost"
          className="justify-start bg-[#f8fafd] shadow-sm hover:bg-[#eef2f8]"
          onPress={() => onSelect(s.stop_id)}
        >
          {s.stop_name} · kod {s.stop_code ?? "—"} · id {s.stop_id}
        </Button>
      ))}
    </div>
  );
}
