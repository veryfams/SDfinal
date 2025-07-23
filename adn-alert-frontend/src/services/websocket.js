let socket;

export const connectWebSocket = (onMessageCallback) => {
  socket = new WebSocket("ws://localhost:8000/ws");

  socket.onopen = () => {
    console.log("🔗 WebSocket conectado al backend FastAPI.");
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    onMessageCallback(data);
  };

  socket.onclose = () => {
    console.log("🚫 WebSocket desconectado.");
  };

  socket.onerror = (error) => {
    console.error("❌ Error WebSocket:", error);
  };
};

export const closeWebSocket = () => {
  if (socket) socket.close();
};
