import React, { useState, useEffect, createContext } from "react";
import { setToken, getToken, removeToken } from "../api/token";
import { useUser } from "../hooks/useUser";

export const AuthContext = createContext({
  auth: undefined,
  login: () => null,
  logout: () => null,
});

export function AuthProvider({ children }) {
  const [auth, setAuth] = useState(undefined);
  const { getMe } = useUser();

  useEffect(() => {
    (async () => {
      const token = getToken();
      if (token) {
        try {
          const me = await getMe(token);
          setAuth({ token, me });
        } catch (error) {
          // Si el token es inválido o expiró, lo borramos
          setAuth(null);
          removeToken();
        }
      } else {
        setAuth(null);
      }
    })();
  }, []);

  const login = async (token) => {
    setToken(token);
    const me = await getMe(token);
    setAuth({ token, me });
  };

  const logout = () => {
    if (auth) {
      setAuth(null);
      removeToken();
    }
  };

  const valueContext = {
    auth,
    login,
    logout,
  };

  // Si auth es undefined, significa que está cargando la sesión
  if (auth === undefined) return null; 

  return (
    <AuthContext.Provider value={valueContext}>
      {children}
    </AuthContext.Provider>
  );
}