let socket;

export const connectWebSocket = (onMessage) => {
  const wsUrl = "ws://127.0.0.1:8000/ws";
  socket = new WebSocket(wsUrl);

  socket.onopen = () => {
    console.log("✅ WebSocket conectado con:", wsUrl);
    // Opcional: enviar algo solo si el servidor lo espera
    // socket.send("cliente conectado");
  };

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      console.log("📩 Mensaje recibido:", data);
      onMessage(data);
    } catch (err) {
      console.warn("⚠️ No se pudo parsear:", event.data);
    }
  };

  socket.onerror = (err) => {
    console.error("❌ Error en WebSocket:", err);
  };

  socket.onclose = (e) => {
    console.warn("🔌 WebSocket cerrado:", e.code, e.reason);
  };
};

export const closeWebSocket = () => {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.close();
    console.log("🔒 WebSocket cerrado manualmente.");
  }
};
