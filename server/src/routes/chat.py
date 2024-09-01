import os
from fastapi import APIRouter, WebSocket, Request, BackgroundTasks, HTTPException, WebSocketDisconnect, Depends
import uuid
import json  # New import for JSON handling
from ..socket.connection import ConnectionManager
from ..socket.utils import get_token
from ..redis.producer import Producer
from ..redis.config import Redis
from ..schema.chat import Chat
from ..redis.stream import StreamConsumer

chat = APIRouter()
manager = ConnectionManager()
redis = Redis()

# @route   POST /token
# @desc    Route to generate chat token
# @access  Public
@chat.post("/token")
async def token_generator(name: str, request: Request):
    if not name:
        raise HTTPException(status_code=400, detail={
            "loc": "name",  "msg": "Enter a valid name"})

    token = str(uuid.uuid4())

    # Create new chat session
    chat_session = Chat(
        token=token,
        messages=[],
        name=name
    )

    # Store chat session in Redis as a JSON string
    redis_client = await redis.create_connection()
    await redis_client.set(str(token), json.dumps(chat_session.model_dump()))

    # Set a timeout for Redis data (1 hour)
    await redis_client.expire(str(token), 3600)

    return chat_session.model_dump()

# @route   GET /refresh_token
# @desc    Route to refresh token
# @access  Public
@chat.get("/refresh_token")
async def refresh_token(request: Request, token: str):
    redis_client = await redis.create_connection()
    data = await redis_client.get(token)

    if data is None:
        raise HTTPException(
            status_code=400, detail="Session expired or does not exist")
    
    # Parse the JSON data retrieved from Redis
    data = json.loads(data)
    return data

# @route   Websocket /chat
# @desc    Socket for chatbot
# @access  Public
@chat.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket, token: str = Depends(get_token)):
    # Accept the WebSocket connection
    await websocket.accept()
    
    redis_client = await redis.create_connection()
    producer = Producer(redis_client)
    json_client = redis.create_rejson_connection()
    consumer = StreamConsumer(redis_client)

    try:
        while True:
            # Receive message from WebSocket
            data = await websocket.receive_text()
            stream_data = {str(token): str(data)}
            await producer.add_to_stream(stream_data, "message_channel")
            
            # Consume message from stream
            response = await consumer.consume_stream(stream_channel="response_channel", block=0)
            print(response)

            for stream, messages in response:
                for message in messages:
                    response_token = [k.decode('utf-8') for k, v in message[1].items()][0]
                    
                    if token == response_token:
                        response_message = [v.decode('utf-8') for k, v in message[1].items()][0]
                        print(message[0].decode('utf-8'))
                        print(token)
                        print(response_token)

                        await websocket.send_text(response_message)

                    await consumer.delete_message(stream_channel="response_channel", message_id=message[0].decode('utf-8'))

    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()


