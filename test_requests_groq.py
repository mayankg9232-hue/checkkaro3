import requests
import json
import time

import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")
url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "openai/gpt-oss-120b",
    "messages": [
        {"role": "user", "content": "Summarize this: Academic and Grading Policy 2026 for Scaler School of Technology. Key points: Relative grading, CGPA scale 10.0, Attendance minimum 85%."}
    ],
    "temperature": 0.2
}

t0 = time.time()
try:
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    print("Status code:", resp.status_code)
    print("Time taken:", time.time() - t0)
    print("Response:\n", resp.json()["choices"][0]["message"]["content"][:200])
except Exception as e:
    print("Requests error:", e)
