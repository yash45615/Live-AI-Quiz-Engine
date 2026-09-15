from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):
        self.active_connections: dict[
            str,
            list[WebSocket]
        ] = {}

    async def connect(
        self,
        session_code: str,
        websocket: WebSocket
    ):

        await websocket.accept()

        if session_code not in self.active_connections:
            self.active_connections[session_code] = []

        self.active_connections[session_code].append(
            websocket
        )

    def disconnect(
        self,
        session_code: str,
        websocket: WebSocket
    ):

        if session_code not in self.active_connections:
            return

        if websocket in self.active_connections[session_code]:
            self.active_connections[session_code].remove(
                websocket
            )

        if not self.active_connections[session_code]:
            del self.active_connections[session_code]

    async def broadcast(
        self,
        session_code: str,
        message: dict
    ):

        connections = self.active_connections.get(
            session_code,
            []
        )

        disconnected = []

        for connection in connections:

            try:
                await connection.send_json(message)

            except Exception:
                disconnected.append(connection)

        for connection in disconnected:

            self.disconnect(
                session_code,
                connection
            )


manager = ConnectionManager()