import { afterEach, describe, expect, it, vi } from "vitest";
import { apiClient, ApiError } from "./apiClient";

describe("apiClient", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("returns parsed JSON on a successful response", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockImplementation(
        async () => new Response(JSON.stringify({ message: "ok" }), { status: 200 })
      )
    );

    const result = await apiClient.get<{ message: string }>("/health/");

    expect(result).toEqual({ message: "ok" });
  });

  it("throws a typed ApiError using the backend's error contract", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockImplementation(
        async () =>
          new Response(
            JSON.stringify({
              code: "NOT_FOUND",
              message: "The requested resource was not found.",
              details: {},
            }),
            { status: 404 }
          )
      )
    );

    await expect(apiClient.get("/missing/")).rejects.toBeInstanceOf(ApiError);
    await expect(apiClient.get("/missing/")).rejects.toMatchObject({
      code: "NOT_FOUND",
      status: 404,
    });
  });

  it("falls back to a generic error when the response isn't in the expected shape", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockImplementation(
        async () => new Response("<html>Bad Gateway</html>", { status: 502 })
      )
    );

    await expect(apiClient.get("/health/")).rejects.toMatchObject({
      code: "UNKNOWN_ERROR",
      status: 502,
    });
  });

  it("attaches X-CSRFToken from the cookie on unsafe methods, but not on GET", async () => {
    document.cookie = "csrftoken=test-csrf-value";
    const fetchMock = vi.fn().mockImplementation(
      async () => new Response(JSON.stringify({ ok: true }), { status: 200 })
    );
    vi.stubGlobal("fetch", fetchMock);

    await apiClient.post("/auth/login/", { email: "a@example.com", password: "pw" });
    await apiClient.get("/auth/me/");

    const [postCall, getCall] = fetchMock.mock.calls;
    expect((postCall[1].headers as Record<string, string>)["X-CSRFToken"]).toBe(
      "test-csrf-value"
    );
    expect((getCall[1].headers as Record<string, string>)["X-CSRFToken"]).toBeUndefined();

    document.cookie = "csrftoken=; expires=Thu, 01 Jan 1970 00:00:00 UTC";
  });
});
