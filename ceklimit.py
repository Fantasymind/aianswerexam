import requests
import json

response = requests.get(
  url="https://openrouter.ai/api/v1/auth/key",
  headers={
    "Authorization": f"Bearer busssssss"
  }
)

print(json.dumps(response.json(), indent=2))
