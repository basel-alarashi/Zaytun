import type { RouteObject } from "react-router-dom";
import { RequireAuth } from "../features/auth/RequireAuth";
import { DashboardPage } from "../pages/DashboardPage";

export const dashboardRoutes: RouteObject[] = [
  {
    path: "/dashboard",
    element: (
      <RequireAuth>
        <DashboardPage />
      </RequireAuth>
    ),
  },
];