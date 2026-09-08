import { afterEach, describe, expect, it, vi } from "vitest";
import { apiClient, ApiError } from "../lib/apiClient";

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
});
