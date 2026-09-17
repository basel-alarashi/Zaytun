import React, { useCallback, useEffect, useState } from "react";
import type { ApiErrorPayload } from "../types/errors";

interface AsyncState<T> {
  data: T | null;
  loading: boolean;
  error: ApiErrorPayload | null;
}

export function useAsync<T>(fn: () => Promise<T>, deps: React.DependencyList = []) {
  const [state, setState] = useState<AsyncState<T>>({
    data: null,
    loading: true,
    error: null,
  });

  const run = useCallback(() => {
    setState({ data: null, loading: true, error: null });
    fn()
      .then((data) => setState({ data, loading: false, error: null }))
      .catch((err) => {
        const payload: ApiErrorPayload = err?.payload ?? {
          code: "UNKNOWN_ERROR",
          message: "Something went wrong. Please try again.",
        };
        setState({ data: null, loading: false, error: payload });
      });
    // eslint-disable-next-line react-hooks/exhaustive-deps, react-hooks/use-memo
  }, deps);

  useEffect(() => {
    run();
  }, [run]);

  return { ...state, refetch: run };
}