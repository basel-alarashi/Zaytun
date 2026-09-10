import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { apiClient, ApiError } from "../lib/apiClient";
import { useAuth } from "../features/auth/useAuth";

interface HealthResponse {
  message: string;
}

type HealthState =
  | { status: "loading" }
  | { status: "success"; message: string }
  | { status: "error"; message: string };

export function HomePage() {
  const { user, logout } = useAuth();
  const [health, setHealth] = useState<HealthState>({ status: "loading" });

  useEffect(() => {
    let cancelled = false;

    apiClient
      .get<HealthResponse>("/health/")
      .then((data) => {
        if (!cancelled) setHealth({ status: "success", message: data.message });
      })
      .catch((error: unknown) => {
        if (cancelled) return;
        const message =
          error instanceof ApiError ? error.message : "Could not reach the Zaytun API.";
        setHealth({ status: "error", message });
      });

    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <main>
      <h1>Zaytun</h1>
      {health.status === "loading" && <p role="status">Checking API connection…</p>}
      {health.status === "success" && <p role="status">{health.message}</p>}
      {health.status === "error" && <p role="alert">{health.message}</p>}

      {user ? (
        <p>
          Signed in as {user.email} ({user.role}).{" "}
          <button type="button" onClick={() => void logout()}>
            Log out
          </button>
        </p>
      ) : (
        <p>
          <Link to="/login">Log in</Link> or <Link to="/register">Register</Link>
        </p>
      )}
    </main>
  );
}