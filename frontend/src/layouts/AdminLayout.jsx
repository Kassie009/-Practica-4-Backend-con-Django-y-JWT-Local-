import { Login } from "../pages/common";
import { useAuth } from "../hooks/useAuth";

export function AdminLayout({ children }) {
  const { auth } = useAuth();

  // Si auth es undefined (cargando) o null (no logueado), muestra el Login
  if (!auth) return <Login />;

  return <div>{children}</div>;
}