"""
Check connectivity to Gemini. No external dependencies.

PROMPT> export GEMINI_API_KEY=your-gemini-api-key-here
PROMPT> python -m planexe.proof_of_concepts.run_ping_simple
"""
import requests
import json
import os

model_name = "gemini-2.0-flash-exp"
gemini_api_key = os.getenv("GEMINI_API_KEY")

print("connecting to gemini...")
response = requests.post(
  url=f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={gemini_api_key}",
  headers={
    "Content-Type": "application/json"
  },
  data=json.dumps({
    "contents": [
      {
        "parts": [
          {
            "text": "List names of 3 planets in the solar system. Comma separated. No other text."
          }
        ]
      }
    ]
  })
)
print(f"response:\n{response.json()}")
