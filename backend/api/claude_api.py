import requests

CLAUDE_API_KEY = "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"

API_URL = "https://api.anthropic.com/v1/messages"


def ask_claude(prompt):
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    data = {
        "model": "claude-3-opus-20240229",
        "max_tokens": 256,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(API_URL, headers=headers, json=data)
    try:
        return response.json()["content"]
    except Exception:
        return {"error": response.text} 