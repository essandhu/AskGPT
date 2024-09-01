import json

class Cache:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    async def get_chat_history(self, token: str):
        data = await self.redis_client.get(str(token))
        return json.loads(data) if data else None

    async def add_message_to_cache(self, token: str, source: str, message_data: dict):
        """Assuming this method was part of the original code."""
        chat_history = await self.get_chat_history(token)
        if chat_history is None:
            chat_history = {"messages": []}
        chat_history["messages"].append({"source": source, **message_data})
        await self.redis_client.set(str(token), json.dumps(chat_history))
