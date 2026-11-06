import React, { useState, useEffect } from "react";
import { Button, Card } from "semantic-ui-react";
import { useAuth } from "../../hooks/useAuth";

export function Dashboard() {
  const { logout, auth } = useAuth();
  const user = auth?.me; 
  
  // Estados para la API de terceros
  const [advice, setAdvice] = useState("");
  const [loading, setLoading] = useState(true);

  // Consumo de la API de terceros (Advice Slip API)
  useEffect(() => {
    fetch("https://api.adviceslip.com/advice")
      .then((response) => response.json())
      .then((data) => {
        setAdvice(data.slip.advice);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error al cargar la API:", error);
        setLoading(false);
      });
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Dashboard Page</h1>
      <h3>Bienvenido {user?.email}</h3>
      <Button type="submit" content="Cerrar Sesión" onClick={logout} secondary />

      <hr style={{ margin: "30px 0" }} />

      {/* Widget de API de Terceros */}
      <h2>Consejo del día (API Externa)</h2>
      <Card fluid>
        <Card.Content>
          {loading ? (
            <p>Cargando consejo...</p>
          ) : (
            <Card.Description style={{ fontSize: "1.2rem", fontStyle: "italic" }}>
              "{advice}"
            </Card.Description>
          )}
        </Card.Content>
      </Card>
    </div>
  );
}