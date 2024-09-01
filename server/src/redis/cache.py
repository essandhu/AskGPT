import json  # New import for JSON handling

class Cache:
    def __init__(self, json_client):
        self.json_client = json_client

    async def get_chat_history(self, token: str):
        # Retrieve the JSON string from Redis
        data = await self.json_client.get(str(token))
        
        # Return None if no data is found
        if data is None:
            return None
        
        # Deserialize the JSON string to a Python dictionary
        return json.loads(data)

    async def add_message_to_cache(self, token: str, source: str, message_data: dict):
        # Retrieve current chat history
        data = await self.get_chat_history(token)
        
        if data:
            data['messages'].append({"source": source, "msg": message_data['msg']})
        else:
            # Create a new chat history if none exists
            data = {
                "token": token,
                "messages": [{"source": source, "msg": message_data['msg']}]
            }
        
        # Store the updated chat history in Redis
        await self.json_client.set(str(token), json.dumps(data))
