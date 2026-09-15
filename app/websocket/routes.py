from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.websocket.manager import manager


router = APIRouter()


@router.websocket("/ws/{session_code}")
async def websocket_endpoint(
    websocket: WebSocket,
    session_code: str
):

    await manager.connect(
        session_code,
        websocket
    )

    await manager.broadcast(
        session_code,
        {
            "type": "system",
            "message": f"A user connected to {session_code}"
        }
    )

    try:

        while True:

            data = await websocket.receive_json()

            message_type = data.get("type")

            if message_type == "ping":

                await websocket.send_json({
                    "type": "pong"
                })

            elif message_type == "chat":

                await manager.broadcast(
                    session_code,
                    {
                        "type": "chat",
                        "message": data.get(
                            "message",
                            ""
                        )
                    }
                )

            elif message_type == "next_question":

                await manager.broadcast(
                    session_code,
                    {
                        "type": "question_update",
                        "question_id": data.get(
                            "question_id"
                        ),
                        "question_number": data.get(
                            "question_number",
                            0
                        )
                    }
                )

    except WebSocketDisconnect:

        manager.disconnect(
            session_code,
            websocket
        )

        await manager.broadcast(
            session_code,
            {
                "type": "system",
                "message": "A user disconnected"
            }
        )