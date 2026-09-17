import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { RequireAuth } from "../RequireAuth";
import { useAuth } from "../useAuth";

vi.mock("../useAuth", () => ({
  useAuth: vi.fn(),
}));

function renderWithRouter(initialPath: string) {
  return render(
    <MemoryRouter initialEntries={[initialPath]}>
      <Routes>
        <Route path="/login" element={<p>Login page</p>} />
        <Route
          path="/protected"
          element={
            <RequireAuth>
              <p>Protected content</p>
            </RequireAuth>
          }
        />
      </Routes>
    </MemoryRouter>
  );
}

describe("RequireAuth", () => {
  it("shows a loading indicator while auth status is resolving", () => {
    vi.mocked(useAuth).mockReturnValue({
      status: "loading",
      user: null,
      login: vi.fn(),
      register: vi.fn(),
      logout: vi.fn(),
    });

    renderWithRouter("/protected");

    expect(screen.getAllByRole("status")[0]).toBeInTheDocument();
  });

  it("redirects to /login when anonymous", () => {
    vi.mocked(useAuth).mockReturnValue({
      status: "anonymous",
      user: null,
      login: vi.fn(),
      register: vi.fn(),
      logout: vi.fn(),
    });

    renderWithRouter("/protected");

    expect(screen.getAllByText("Login page")[0]).toBeInTheDocument();
  });

  it("renders children when authenticated and role isn't restricted", () => {
    vi.mocked(useAuth).mockReturnValue({
      status: "authenticated",
      user: {
        id: 1,
        email: "consumer@example.com",
        first_name: "",
        last_name: "",
        role: "CONSUMER",
        date_joined: "2026-01-01T00:00:00Z",
      },
      login: vi.fn(),
      register: vi.fn(),
      logout: vi.fn(),
    });

    renderWithRouter("/protected");

    expect(screen.getAllByText("Protected content")[0]).toBeInTheDocument();
  });
});