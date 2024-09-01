import os
import json
from dotenv import load_dotenv
import redis.asyncio as redis

load_dotenv()

class Redis():
    def __init__(self):
        """Initialize connection parameters."""
        self.REDIS_URL = os.getenv('REDIS_URL')
        self.REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
        self.REDIS_USER = os.getenv('REDIS_USER')
        self.REDIS_HOST = os.getenv('REDIS_HOST')
        self.REDIS_PORT = os.getenv('REDIS_PORT')

        # URL for Redis connection
        self.connection_url = f"redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    async def create_connection(self):
        """Create an async Redis connection."""
        self.connection = redis.Redis.from_url(
            url=self.connection_url,
            decode_responses=True
        )
        # Ping the connection to ensure it works
        await self.connection.ping()
        return self.connection

    async def set_json(self, key, value):
        """Store JSON data in Redis."""
        json_data = json.dumps(value)
        await self.connection.set(key, json_data)

    async def get_json(self, key):
        """Retrieve JSON data from Redis."""
        json_data = await self.connection.get(key)
        if json_data:
            return json.loads(json_data)
        return None
