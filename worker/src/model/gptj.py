import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

class GPT:
    def __init__(self):
        self.url = os.environ.get('MODEL_URL')
        self.headers = {
            "Authorization": f"Bearer {os.environ.get('HUGGINFACE_INFERENCE_TOKEN')}",
            "Content-Type": "application/json"
        }
        self.payload = {
            "inputs": "",
            "parameters": {
                "return_full_text": False,
                "use_cache": True,
                "max_new_tokens": 25
            }
        }

    def query(self, input: str) -> str:
        self.payload["inputs"] = f"Human: {input} Bot:"
        data = json.dumps(self.payload)
        response = requests.request(
            "POST", self.url, headers=self.headers, data=data)
        
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response content: {response.content.decode('utf-8')}")
            return "Error: Failed to get a valid response from the server"
        
        try:
            data = json.loads(response.content.decode("utf-8"))
            print(data)  # Debugging line to print the response data
            if isinstance(data, list) and len(data) > 0 and 'generated_text' in data[0]:
                text = data[0]['generated_text']
                res = str(text.split("Human:")[0]).strip("\n").strip()
                return res
            else:
                print("Unexpected response format:", data)
                return "Error: Unexpected response format"
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            print(f"Response content: {response.content.decode('utf-8')}")
            return "Error: Failed to decode JSON"
        except KeyError as e:
            print("KeyError:", e)
            return "Error: Missing expected key in response"

if __name__ == "__main__":
    GPT().query("Will artificial intelligence help humanity conquer the universe?")