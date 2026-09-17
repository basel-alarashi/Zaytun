import type { RouteObject } from "react-router-dom";
import { publicRoutes } from "./publicRoutes";
import { dashboardRoutes } from "./dashboardRoutes";
import { farmerRoutes } from "./farmerRoutes";

// Adding a new domain (e.g. consumerRoutes in Stage D) means: create the
// file, add it to this array. App.tsx never needs to change again.
export const appRoutes: RouteObject[] = [
  ...publicRoutes,
  ...dashboardRoutes,
  ...farmerRoutes,
];