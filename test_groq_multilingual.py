from groq import Groq
import json

import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

sample_text = """
INCOME TAX DEPARTMENT - GOVERNMENT OF INDIA
Intimation under Section 143(1) of the Income-tax Act, 1961
Assessment Year: 2025-26 | PAN: ABCDE1234F
Outstanding net demand payable: Rs 4,500
Pay within 30 days of receipt via Challan ITNS 280 / e-Pay Tax.
Failure to pay within 30 days will attract additional interest under Section 220(2) at 1% per month.
Required documents: Form 16 / TDS certificates, Bank statement.
"""

system_prompt = """You are an expert Indian legal, administrative, and government document assistant.
Analyze the provided document text and produce a plain-language breakdown in Hindi (हिंदी).
Respond ONLY with a valid JSON object (no markdown, no other text) with keys:
- "doc_type"
- "summary"
- "steps" (list)
- "deadlines" (list of objects with "date" and "description")
- "required_documents" (list)
- "risks" (list)
All values must be in Hindi (हिंदी)."""

for m in ["qwen/qwen3.6-27b", "openai/gpt-oss-120b"]:
    try:
        resp = client.chat.completions.create(
            model=m,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Document:\n{sample_text}"}
            ],
            temperature=0.2
        )
        content = resp.choices[0].message.content
        print(f"--- Model: {m} ---")
        print("Raw response:\n", content[:300])
        parsed = json.loads(content.strip().replace("```json", "").replace("```", ""))
        print("Successfully parsed JSON keys:", list(parsed.keys()))
        print("Sample Summary (Hindi):", parsed["summary"])
        break
    except Exception as e:
        print(f"Model {m} error:", e)
