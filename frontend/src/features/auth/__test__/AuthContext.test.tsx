import { act, renderHook, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { ReactNode } from "react";
import { AuthProvider } from "../AuthProvider";
import { useAuth } from '../useAuth';
import { authApi } from "../authApi";
import { ApiError } from "../../../lib/apiClient";

vi.mock("../authApi", () => ({
  authApi: {
    ensureCsrfCookie: vi.fn(),
    me: vi.fn(),
    login: vi.fn(),
    register: vi.fn(),
    logout: vi.fn(),
  },
}));

const wrapper = ({ children }: { children: ReactNode }) => (
  <AuthProvider>{children}</AuthProvider>
);

const CONSUMER = {
  id: 1,
  email: "consumer@example.com",
  first_name: "",
  last_name: "",
  role: "CONSUMER" as const,
  date_joined: "2026-01-01T00:00:00Z",
};

describe("AuthProvider / useAuth", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("resolves to authenticated when a session already exists", async () => {
    vi.mocked(authApi.ensureCsrfCookie).mockResolvedValue({ detail: "ok" });
    vi.mocked(authApi.me).mockResolvedValue(CONSUMER);

    const { result } = renderHook(() => useAuth(), { wrapper });

    expect(result.current.status).toBe("loading");
    await waitFor(() => expect(result.current.status).toBe("authenticated"));
    expect(result.current.user?.email).toBe("consumer@example.com");
  });

  it("resolves to anonymous when there is no session", async () => {
    vi.mocked(authApi.ensureCsrfCookie).mockResolvedValue({ detail: "ok" });
    vi.mocked(authApi.me).mockRejectedValue(
      new ApiError(401, { code: "UNAUTHENTICATED", message: "Authentication required." })
    );

    const { result } = renderHook(() => useAuth(), { wrapper });

    await waitFor(() => expect(result.current.status).toBe("anonymous"));
    expect(result.current.user).toBeNull();
  });

  it("login() updates user and status", async () => {
    vi.mocked(authApi.ensureCsrfCookie).mockResolvedValue({ detail: "ok" });
    vi.mocked(authApi.me).mockRejectedValue(
      new ApiError(401, { code: "UNAUTHENTICATED", message: "Authentication required." })
    );
    vi.mocked(authApi.login).mockResolvedValue({ ...CONSUMER, role: "FARMER" });

    const { result } = renderHook(() => useAuth(), { wrapper });
    await waitFor(() => expect(result.current.status).toBe("anonymous"));

    await act(async () => {
      await result.current.login({ email: "farmer@example.com", password: "pw" });
    });

    expect(result.current.status).toBe("authenticated");
    expect(result.current.user?.role).toBe("FARMER");
  });

  it("logout() clears user and status", async () => {
    vi.mocked(authApi.ensureCsrfCookie).mockResolvedValue({ detail: "ok" });
    vi.mocked(authApi.me).mockResolvedValue(CONSUMER);
    vi.mocked(authApi.logout).mockResolvedValue(undefined);

    const { result } = renderHook(() => useAuth(), { wrapper });
    await waitFor(() => expect(result.current.status).toBe("authenticated"));

    await act(async () => {
      await result.current.logout();
    });

    expect(result.current.status).toBe("anonymous");
    expect(result.current.user).toBeNull();
  });
});