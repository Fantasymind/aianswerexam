import requests
import json

response = requests.get(
  url="https://openrouter.ai/api/v1/auth/key",
  headers={
    "Authorization": f"Bearer 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"
  }
)

print(json.dumps(response.json(), indent=2))
