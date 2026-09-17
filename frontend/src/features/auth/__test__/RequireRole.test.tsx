import { render, screen, cleanup } from "@testing-library/react";
import { MemoryRouter, Routes, Route } from "react-router-dom";
import { vi, describe, it, expect, beforeEach, afterEach } from "vitest";
import { RequireRole } from "../RequireRole";
import { useAuth } from "../useAuth";
import type { AuthContextValue } from "../types";

// 1. Properly mock useAuth
vi.mock("../useAuth", () => ({
  useAuth: vi.fn(),
}));

// 2. Properly mock RequireAuth as a plain component wrapper
vi.mock("../RequireAuth", () => ({
  RequireAuth: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

const mockUseAuth = vi.mocked(useAuth);

function renderWithRole(role: string | null, allowedRoles: ("FARMER" | "CONSUMER" | "ADMIN")[]) {
  // Clear any existing mounted trees before re-rendering
  cleanup();

  mockUseAuth.mockReturnValue({
    user: role ? { id: 1, role } : null,
  } as AuthContextValue);

  return render(
    <MemoryRouter initialEntries={["/farmer/products"]}>
      <Routes>
        <Route
          path="/farmer/products"
          element={
            <RequireRole allowedRoles={allowedRoles}>
              <div>Farmer Products Page</div>
            </RequireRole>
          }
        />
        <Route path="/dashboard" element={<div>Dashboard Page</div>} />
      </Routes>
    </MemoryRouter>
  );
}

describe("RequireRole", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    cleanup();
  });

  it("renders children when the user has an allowed role", () => {
    renderWithRole("FARMER", ["FARMER"]);
    expect(screen.getByText("Farmer Products Page")).toBeInTheDocument();
  });

  it("redirects to /dashboard when the user has a disallowed role", () => {
    renderWithRole("CONSUMER", ["FARMER"]);

    expect(screen.getByText("Dashboard Page")).toBeInTheDocument();
    expect(screen.queryByText("Farmer Products Page")).not.toBeInTheDocument();
  });

  it("renders nothing while user is not yet resolved", () => {
    renderWithRole(null, ["FARMER"]);

    expect(screen.queryByText("Farmer Products Page")).not.toBeInTheDocument();
    expect(screen.queryByText("Dashboard Page")).not.toBeInTheDocument();
  });
});