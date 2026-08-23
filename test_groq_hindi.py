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
Outstanding net demand payable: ₹ 4,500
Pay within 30 days of receipt via Challan ITNS 280 / e-Pay Tax.
Failure to pay within 30 days will attract additional interest under Section 220(2) at 1% per month.
Required documents: Form 16 / TDS certificates, Bank statement.
"""

system_prompt = """You are an expert Indian legal, administrative, and government document assistant.
Analyze the provided document text and produce a plain-language breakdown in Hindi (हिंदी).
You MUST respond ONLY with a single valid JSON object.
The JSON object must contain EXACTLY these keys:
- "doc_type": string
- "summary": string
- "steps": array of strings
- "deadlines": array of objects [{"date": string, "description": string}]
- "required_documents": array of strings
- "risks": array of strings
All text values in the JSON MUST be written in Hindi (हिंदी)."""

resp = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Document content:\n{sample_text}"}
    ],
    response_format={"type": "json_object"}
)

print("Groq Response in Hindi:")
print(resp.choices[0].message.content)
