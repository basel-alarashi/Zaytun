import { useEffect, useState } from "react";
import { apiClient, ApiError } from "./lib/apiClient";
import "./App.css";

interface HealthResponse {
  message: string;
}

type HealthState =
  | { status: "loading" }
  | { status: "success"; message: string }
  | { status: "error"; message: string };

function App() {
  const [health, setHealth] = useState<HealthState>({ status: "loading" });

  useEffect(() => {
    let cancelled = false;

    apiClient
      .get<HealthResponse>("health/")
      .then((data) => {
        if (!cancelled) setHealth({ status: "success", message: data.message });
      })
      .catch((error: unknown) => {
        if (cancelled) return;
        const message =
          error instanceof ApiError
            ? error.message
            : "Could not reach the Zaytun API.";
        setHealth({ status: "error", message });
      });

    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <main>
      <h1>Zaytun</h1>
      {health.status === "loading" && (
        <p role="status">Checking API connection…</p>
      )}
      {health.status === "success" && <p role="status">{health.message}</p>}
      {health.status === "error" && <p role="alert">{health.message}</p>}
    </main>
  );
}

export default App;
