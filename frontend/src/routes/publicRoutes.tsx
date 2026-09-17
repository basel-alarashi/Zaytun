import type { RouteObject } from "react-router-dom";
import { HomePage } from "../pages/auth/HomePage";
import { LoginPage } from "../pages/auth/LoginPage";
import { RegisterPage } from "../pages/auth/RegisterPage";

export const publicRoutes: RouteObject[] = [
  { path: "/", element: <HomePage /> },
  { path: "/login", element: <LoginPage /> },
  { path: "/register", element: <RegisterPage /> },
];