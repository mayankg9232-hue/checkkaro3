import json
import re
from groq import Groq
from logic.llm_calls import clean_json_response, normalize_analysis_dict

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
Analyze the provided document text and produce a plain-language breakdown in Kannada (ಕನ್ನಡ).
Respond ONLY with a valid JSON object (no markdown, no preamble) with keys:
- "doc_type": string
- "summary": string
- "steps": array of strings
- "deadlines": array of objects [{"date": string, "description": string}]
- "required_documents": array of strings
- "risks": array of strings
All values must be in Kannada (ಕನ್ನಡ)."""

resp = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Document content:\n{sample_text}"}
    ],
    temperature=0.1
)

content = resp.choices[0].message.content
print("Length of response:", len(content))
parsed = clean_json_response(content)
if parsed:
    normalized = normalize_analysis_dict(parsed)
    print("Successfully parsed & normalized Groq JSON:")
    print("doc_type:", normalized["doc_type"].encode("ascii", "replace").decode())
    print("steps count:", len(normalized["steps"]))
    print("deadlines count:", len(normalized["deadlines"]))
    print("risks count:", len(normalized["risks"]))
else:
    print("Failed to clean JSON. Raw content preview:", content[:200])
