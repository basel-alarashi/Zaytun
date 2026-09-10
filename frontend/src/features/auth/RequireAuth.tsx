import type { ReactNode } from "react";
import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "./useAuth";
import type { User } from "./types";

interface RequireAuthProps {
  children: ReactNode;
  allowedRoles?: Array<User["role"]>;
}

export function RequireAuth({ children, allowedRoles }: RequireAuthProps) {
  const { status, user } = useAuth();
  const location = useLocation();

  if (status === "loading") {
    return <p role="status">Loading…</p>;
  }

  if (status === "anonymous" || !user) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return <Navigate to="/" replace />;
  }

  return <>{children}</>;
}