import { useState } from "react";
import { Spinner } from "@heroui/react";

import { fetchStats, fetchStops } from "./api";
import { SearchForm } from "./components/SearchForm";
import { StatsCard } from "./components/StatsCard";
import { StopList } from "./components/StopList";
import { useAsync } from "./useAsync";

export default function App() {
  const [query, setQuery] = useState("");
  const stops = useAsync(fetchStops);
  const stats = useAsync(fetchStats);

  function handleSearch() {
    stats.reset();
    void stops.run(query);
  }

  const error = stops.error ?? stats.error;

  return (
    <div className="mx-auto flex max-w-3xl flex-col gap-6 p-6">
      <header>
        <h1 className="text-2xl font-bold">Rozkład jazdy</h1>
      </header>

      <SearchForm value={query} onChange={setQuery} onSubmit={handleSearch} />

      {error && <p className="text-red-500">{error}</p>}

      {stops.loading && <Spinner />}
      {stops.data?.length === 0 && (
        <p className="text-gray-500">Nie znaleziono przystanków.</p>
      )}
      {stops.data && stops.data.length > 0 && (
        <StopList stops={stops.data} onSelect={stats.run} />
      )}

      {stats.loading && <Spinner />}
      {stats.data && <StatsCard stats={stats.data} />}
    </div>
  );
}
