import {
  useCallback,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { AuthContext } from "./AuthContext";
import { authApi, type LoginInput, type RegisterInput } from "./authApi";
import type { User, AuthStatus } from "./types";

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [status, setStatus] = useState<AuthStatus>("loading");

  useEffect(() => {
    let cancelled = false;

    async function bootstrap() {
      try {
        // Ensures the csrftoken cookie exists before any POST is attempted
        // (login/register enforce CSRF even pre-session — see ADR-007).
        await authApi.ensureCsrfCookie();
      } catch {
        // Non-fatal: the app should still boot; a later unsafe request
        // would surface a clear 403 if this genuinely failed.
      }

      try {
        const currentUser = await authApi.me();
        if (!cancelled) {
          setUser(currentUser);
          setStatus("authenticated");
        }
      } catch {
        if (!cancelled) {
          setUser(null);
          setStatus("anonymous");
        }
      }
    }

    bootstrap();
    return () => {
      cancelled = true;
    };
  }, []);

  const login = useCallback(async (data: LoginInput) => {
    const loggedInUser = await authApi.login(data);
    setUser(loggedInUser);
    setStatus("authenticated");
  }, []);

  const register = useCallback(async (data: RegisterInput) => {
    const newUser = await authApi.register(data);
    setUser(newUser);
    setStatus("authenticated");
  }, []);

  const logout = useCallback(async () => {
    await authApi.logout();
    setUser(null);
    setStatus("anonymous");
  }, []);

  const value = useMemo(
    () => ({ user, status, login, register, logout }),
    [user, status, login, register, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
