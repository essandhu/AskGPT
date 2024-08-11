from fastapi import WebSocket, status, Query
from typing import Optional
from ..redis.config import Redis

async def get_token(
    websocket: WebSocket,
    token: Optional[str] = Query(None),
):
    
    if token is None or token == "":
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    redis_client = await Redis.create_connection()
    doesExist = await redis_client.exists(token)

    if doesExist == 1:
        return token
    else:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Session not authenticated or expired token")
