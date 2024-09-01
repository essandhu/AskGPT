from fastapi import WebSocket, HTTPException
from ..redis.config import Redis

redis = Redis()

async def get_token(websocket: WebSocket):
    query_params = dict(websocket.query_params)
    token = query_params.get('token')
    
    if not token:
        raise HTTPException(status_code=400, detail="Token is required")
    
    # Validate token with Redis
    redis_client = await redis.create_connection()
    exists = await redis_client.exists(token)
    
    if not exists:
        raise HTTPException(status_code=403, detail="Invalid or expired token")
    
    return token
