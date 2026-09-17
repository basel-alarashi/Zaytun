import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";
import { LoginPage } from "../LoginPage";
import { useAuth } from "../../../features/auth/useAuth";
import { ApiError } from "../../../lib/apiClient";

vi.mock("../../../features/auth/useAuth", () => ({
  useAuth: vi.fn(),
}));

describe("LoginPage", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("calls login with the entered credentials on submit", async () => {
    const login = vi.fn().mockResolvedValue(undefined);
    vi.mocked(useAuth).mockReturnValue({
      status: "anonymous",
      user: null,
      login,
      register: vi.fn(),
      logout: vi.fn(),
    });

    const user = userEvent.setup();
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    );

    await user.type(screen.getAllByLabelText(/email/i)[0], "consumer@example.com");
    await user.type(screen.getAllByLabelText(/password/i)[0], "Str0ng-Passw0rd!");
    await user.click(screen.getAllByRole("button", { name: /log in/i })[0]);

    expect(login).toHaveBeenCalledWith({
      email: "consumer@example.com",
      password: "Str0ng-Passw0rd!",
    });
  });

  it("shows the server's error message on failed login", async () => {
    const login = vi
      .fn()
      .mockRejectedValue(
        new ApiError(400, {
          code: "VALIDATION_ERROR",
          message: "Unable to log in with the provided credentials.",
        })
      );
    vi.mocked(useAuth).mockReturnValue({
      status: "anonymous",
      user: null,
      login,
      register: vi.fn(),
      logout: vi.fn(),
    });

    const user = userEvent.setup();
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    );

    await user.type(screen.getAllByLabelText(/email/i)[0], "consumer@example.com");
    await user.type(screen.getAllByLabelText(/password/i)[0], "wrong");
    await user.click(screen.getAllByRole("button", { name: /log in/i })[0]);

    // Wait for the error message to appear
    const alert = await screen.findByRole("alert");
    expect(alert).toHaveTextContent(
      "Unable to log in with the provided credentials."
    );
  });
});