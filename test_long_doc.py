from groq import Groq
import traceback

import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

sample_long_text = "ACADEMIC & GRADING POLICY 2026 Grading Policy at Scaler School of Technology\n" * 300
print("Sample text length:", len(sample_long_text))

system_prompt = """You are an expert Indian legal, administrative, and government document assistant.
Analyze the provided document text and produce a comprehensive, plain-language breakdown in English.
You MUST respond ONLY with a single valid JSON object. Do not include introductory text or commentary.
The JSON object must contain EXACTLY these keys:
- "doc_type": A concise classification or title of the document (string)
- "summary": A clear, simple, plain-language summary of what the document is about and what it means (string)
- "steps": A chronological array of clear, actionable steps the recipient must take (array of strings)
- "deadlines": An array of objects, each with "date" (string) and "description" (string). Empty array [] if none.
- "required_documents": An array of documents, proofs, or certificates mentioned or needed (array of strings). Empty array [] if none.
- "risks": An array of critical risks, warnings, penalties, or consequences of non-compliance (array of strings). Empty array [] if none.

All text values in the JSON MUST be written in English."""

user_prompt = f"DOCUMENT CONTENT TO ANALYZE:\n\n{sample_long_text}"

for m in ["openai/gpt-oss-120b", "qwen/qwen3.6-27b", "openai/gpt-oss-20b"]:
    try:
        print(f"Trying model: {m}...")
        resp = client.chat.completions.create(
            model=m,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2
        )
        print("Success! Content length:", len(resp.choices[0].message.content))
        print("Content preview:", resp.choices[0].message.content[:300])
        break
    except Exception as e:
        print(f"Model {m} failed:", e)
        traceback.print_exc()
