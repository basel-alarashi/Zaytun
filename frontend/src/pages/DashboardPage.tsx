import { useAuth } from "../features/auth/useAuth";

export function DashboardPage() {
  const { user } = useAuth();

  return (
    <main>
      <h1>Dashboard</h1>
      <p>
        Welcome, {user?.email}. This is a protected placeholder — real dashboards arrive in
        later sprints.
      </p>
    </main>
  );
}