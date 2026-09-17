import { Navigate } from "react-router-dom";
import { RequireAuth } from "./RequireAuth";
import { useAuth } from "./useAuth";

export type Role = "CONSUMER" | "FARMER" | "ADMIN";

interface RequireRoleProps {
  allowedRoles: Role[];
  children: React.ReactNode;
}

/**
 * Wraps RequireAuth (authentication) and adds a role check on top
 * (authorization). Keeping the two separate means "logged in but
 * wrong role" and "not logged in" can be handled/redirected differently.
 */
export function RequireRole({ allowedRoles, children }: RequireRoleProps) {
  return (
    <RequireAuth>
      <RoleGate allowedRoles={allowedRoles}>{children}</RoleGate>
    </RequireAuth>
  );
}

function RoleGate({ allowedRoles, children }: RequireRoleProps) {
  const { user } = useAuth();

  // RequireAuth guarantees a session exists by the time we render this,
  // but `user` can briefly be null during the initial /auth/me/ resolve.
  if (!user) return null;

  if (!allowedRoles.includes(user.role as Role)) {
    return <Navigate to="/dashboard" replace />;
  }

  return <>{children}</>;
}