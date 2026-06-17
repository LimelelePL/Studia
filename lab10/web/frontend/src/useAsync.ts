import { useCallback, useState } from "react";

interface AsyncState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

const initialState = { data: null, loading: false, error: null } as const;

export function useAsync<T, Args extends unknown[]>(
  fn: (...args: Args) => Promise<T>,
) {
  const [state, setState] = useState<AsyncState<T>>(initialState);

  const run = useCallback(
    async (...args: Args): Promise<void> => {
      setState({ data: null, loading: true, error: null });
      try {
        const data = await fn(...args);
        setState({ data, loading: false, error: null });
      } catch (err) {
        setState({ data: null, loading: false, error: String(err) });
      }
    },
    [fn],
  );

  const reset = useCallback(() => setState(initialState), []);

  return { ...state, run, reset };
}
