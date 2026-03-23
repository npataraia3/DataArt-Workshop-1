from fastapi import WebSocket
from .presence import update_activity

connections = {}

async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    connections[user_id] = websocket

    while True:
        data = await websocket.receive_text()
        update_activity(user_id)

        for conn in connections.values():
            await conn.send_text(data)