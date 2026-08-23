from groq import Groq
from logic.llm_calls import clean_json_response, normalize_analysis_dict
import json

import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key, timeout=30.0)

sample_doc = """
ACADEMIC & GRADING POLICY 2026
Scaler School of Technology
1. Grading Scheme: Scaler School of Technology follows a 10-point Letter Grading System (A+: 10, A: 9, B+: 8, B: 7, C: 6, D: 4, F: 0).
2. Minimum Passing Criteria: Students must achieve at least a 'D' grade (CGPA >= 5.0) in core subjects.
3. Attendance Policy: Minimum 85% attendance is required to be eligible for end-term examinations. Students below 75% will be debarred (Grade 'I').
4. Deadlines: Course registration deadline is August 31, 2026. Late registration with penalty fee of INR 1000 allowed till Sept 7, 2026.
5. Required Documents: Semester transcript request requires Student ID card, Fee clearance certificate, and No-dues form.
6. Academic Integrity & Risks: Plagiarism or cheating in lab assignments results in immediate 'F' grade and disciplinary probation.
"""

system_prompt = """You are an expert document and government process assistant.
Analyze the provided document text and produce a comprehensive, plain-language breakdown in English.
Respond ONLY with a valid JSON object with EXACTLY these keys:
- "doc_type": string
- "summary": string
- "steps": array of strings
- "deadlines": array of objects [{"date": string, "description": string}]
- "required_documents": array of strings
- "risks": array of strings
All text values must be in English."""

resp = client.chat.completions.create(
    model="qwen/qwen3.6-27b",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Document content:\n{sample_doc}"}
    ],
    max_tokens=4096,
    temperature=0.1
)

raw_content = resp.choices[0].message.content
print("RAW OUTPUT LENGTH:", len(raw_content))
print("FINISH REASON:", resp.choices[0].finish_reason)

parsed = clean_json_response(raw_content)
print("PARSED RESULT IS NONE?", parsed is None)
if parsed:
    normalized = normalize_analysis_dict(parsed)
    print("DOC TYPE:", repr(normalized.get("doc_type")))
    print("SUMMARY:", repr(normalized.get("summary")[:120]))
    print("STEPS COUNT:", len(normalized.get("steps", [])))
    print("DEADLINES:", normalized.get("deadlines"))
    print("RISKS:", repr(normalized.get("risks")))
else:
    print("FAILED PARSING. Tail of output:")
    print(repr(raw_content[-500:]))
