import React, { useState, useEffect } from 'react';
import RoleSwitcher from './components/RoleSwitcher';
import CiudadanoView from './views/CiudadanoView';
import BomberoView from './views/BomberoView';
import AdminView from './views/AdminView';
import AlertList from './components/AlertList';
import { connectWebSocket, closeWebSocket } from './services/websocket';

function App() {
  const [role, setRole] = useState("ciudadano");
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    connectWebSocket((data) => {
      const alertaConHora = { ...data, hora: new Date().toISOString() };
      setAlerts((prev) => [...prev, alertaConHora]);
    });

    return () => closeWebSocket();
  }, []);

  // ✅ USAR alertasFiltradas correctamente
  const alertasFiltradas = alerts.filter((a) => {
    if (role === "ciudadano") return true;
    if (role === "bombero") return a.tipo === "incendio" || a.tipo === "inundacion";
    return true; // admin ve todo
  });

  return (
    <div className="container py-4">
      <h1 className="text-center">🌐 Sistema de Alerta de Desastres</h1>
      <RoleSwitcher role={role} setRole={setRole} />

      {role === "ciudadano" && <CiudadanoView />}
      {role === "bombero" && <BomberoView />}
      {role === "admin" && <AdminView />}

      {/* ✅ Aquí se usa alertasFiltradas */}
      <AlertList alerts={alertasFiltradas} role={role} />
    </div>
  );
}

export default App;
