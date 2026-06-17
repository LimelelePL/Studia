export interface Stop {
  stop_id: number;
  stop_code: string | null;
  stop_name: string;
}

export interface Direction {
  direction: string | null;
  count: number;
}

export interface RouteRow {
  route: string;
  direction: string | null;
  count: number;
  first: string;
  last: string;
}

export interface Stats {
  stop: Stop;
  count_routes: number;
  count_departures: number;
  first_departure: string | null;
  last_departure: string | null;
  directions: Direction[];
  by_route: RouteRow[];
}
