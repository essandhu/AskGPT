import os
from dotenv import load_dotenv
import redis.asyncio as aioredis
import json

load_dotenv()

class Redis():
    def __init__(self):
        """Initialize connection"""
        self.REDIS_URL = os.environ['REDIS_URL']
        self.REDIS_PASSWORD = os.environ['REDIS_PASSWORD']
        self.REDIS_USER = os.environ['REDIS_USER']
        self.REDIS_HOST = os.environ['REDIS_HOST']
        self.REDIS_PORT = os.environ['REDIS_PORT']
        self.connection_url = f"redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@{self.REDIS_URL}"

    async def create_connection(self):
        """Create an async Redis connection"""
        self.connection = aioredis.from_url(
            self.connection_url, db=0, encoding="utf-8", decode_responses=True
        )
        return self.connection

    async def set_json(self, key, value):
        """Set a key-value pair in Redis, with the value as a JSON-encoded string"""
        redis_client = await self.create_connection()
        await redis_client.set(key, json.dumps(value))

    async def get_json(self, key):
        """Get a value from Redis and decode the JSON string"""
        redis_client = await self.create_connection()
        value = await redis_client.get(key)
        return json.loads(value) if value else None
