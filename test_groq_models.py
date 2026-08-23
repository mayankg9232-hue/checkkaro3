from groq import Groq

import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

models = ["openai/gpt-oss-120b", "qwen/qwen3.6-27b", "openai/gpt-oss-20b", "groq/compound"]

for m in models:
    try:
        resp = client.chat.completions.create(
            model=m,
            messages=[{"role": "user", "content": "Respond strictly in JSON: {\"status\": \"ok\", \"model\": \"" + m + "\"}"}],
            response_format={"type": "json_object"}
        )
        print(f"Model {m} SUCCESS:")
        print(resp.choices[0].message.content)
        break
    except Exception as e:
        print(f"Model {m} failed:", e)
