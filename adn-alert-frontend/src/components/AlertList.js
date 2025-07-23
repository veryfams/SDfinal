import React from "react";
import moment from "moment";

export default function AlertList({ alerts, role }) {
  return (
    <div className="mt-4">
      <h4>📢 Alertas Recibidas ({alerts.length})</h4>
      <ul className="list-group">
        {alerts.map((alerta, idx) => (
          <li
            key={idx}
            className={`list-group-item list-group-item-${alerta.tipo === "sismo"
              ? "danger"
              : alerta.tipo === "incendio"
              ? "warning"
              : "info"
            }`}
          >
            <strong>{alerta.tipo.toUpperCase()}</strong> en <em>{alerta.region}</em>
            {role === "admin" && (
              <span className="text-muted ms-2">
                ({moment(alerta.hora).format("HH:mm:ss")})
              </span>
            )}
            <br />
            {alerta.mensaje}
          </li>
        ))}
      </ul>
    </div>
  );
}
