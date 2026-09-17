import { useRoutes } from "react-router-dom";
import { AuthProvider } from "./features/auth/AuthProvider";
import { appRoutes } from "./routes";

function AppRoutes() {
  return useRoutes(appRoutes);
}

function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  );
}

export default App;