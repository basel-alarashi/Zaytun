import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import { apiClient, ApiError } from "../lib/apiClient";

vi.mock("../lib/apiClient", async (importOriginal) => {
  const actual = await importOriginal<typeof import("../lib/apiClient")>();
  return {
    ...actual,
    apiClient: { ...actual.apiClient, get: vi.fn() },
  };
});

describe("App", () => {
  afterEach(() => {
    vi.resetAllMocks();
  });

  it("shows the API's health message once the request resolves", async () => {
    vi.mocked(apiClient.get).mockResolvedValue({
      message: "Django API is running healthy!",
    });

    render(<App />);

    // Wait specifically for the text content to appear on screen
    expect(
      await screen.findByText("Django API is running healthy!")
    ).toBeInTheDocument();
  });

  it("shows an error message when the health check fails", async () => {
    vi.mocked(apiClient.get).mockRejectedValue(
      new ApiError(500, {
        code: "SERVER_ERROR",
        message: "An unexpected error occurred.",
      })
    );

    render(<App />);

    // Wait specifically for the error text to appear on screen
    expect(
      await screen.findByText("An unexpected error occurred.")
    ).toBeInTheDocument();
  });
});