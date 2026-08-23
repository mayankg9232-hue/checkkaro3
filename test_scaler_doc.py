from groq import Groq
from logic.llm_calls import clean_json_response, normalize_analysis_dict

import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key, timeout=45.0)

# Simulate a 20,000 character document
doc_text = """
SCALER SCHOOL OF TECHNOLOGY
ACADEMIC & GRADING POLICY GUIDELINES - 2026

1. Overview and Program Structure
Scaler School of Technology (SST) offers an undergraduate program in Computer Science & Artificial Intelligence.
Students are evaluated continuously across assignments, quizzes, labs, midterm exams, and capstone projects.

2. Grading System & Grade Point Scale
The institution operates on a 10.0 Cumulative Grade Point Average (CGPA) scale:
- O (Outstanding): Grade Point 10.0
- A+ (Excellent): Grade Point 9.0
- A (Very Good): Grade Point 8.0
- B+ (Good): Grade Point 7.0
- B (Above Average): Grade Point 6.0
- C (Average / Pass): Grade Point 5.0
- F (Fail): Grade Point 0.0 (Mandatory repeat/supplementary exam)

3. Attendance Regulations
- Mandatory minimum attendance across all lecture and lab sessions is 85%.
- Medical leave allowance up to 10% requires immediate submission of doctor prescription and hospital certificate within 7 calendar days.
- Students with attendance below 75% will be summarily debarred from sitting in end-semester examinations with an 'I' (Incomplete/Debarred) status.

4. Academic Calendar & Critical Deadlines
- Course Add/Drop Window: 10-August-2026 to 20-August-2026.
- Course Registration Final Date: 31-August-2026.
- Midterm Assessment Window: 15-October-2026 to 22-October-2026.
- Final Term Examination: 10-December-2026 to 20-December-2026.

5. Required Documents for Certification & Formal Requests
- Valid Scaler Student Identity Card.
- Official Semester Fee Payment Challan or Receipt.
- No-Dues Clearance signed by Academic Coordinator and Hostel Warden.

6. Plagiarism, Cheating & Serious Risks
- Strict zero-tolerance plagiarism threshold: Any submitted code matching > 15% with internet or peer repositories via automated detector will receive 0 marks and a formal written reprimand.
- Second infraction results in immediate suspension for 1 semester.
""" + ("\nAdditional curriculum details and supplementary guidelines for electives.\n" * 150)

print("Test document size:", len(doc_text), "characters")

system_prompt = """You are an expert document analysis assistant.
Analyze the provided document text and produce a comprehensive, accurate plain-language breakdown in English.
Respond ONLY with a valid JSON object. No other text.
The JSON object must contain EXACTLY these keys:
- "doc_type": concise title/type of document (string)
- "summary": detailed plain-language summary of what the document is about and what it means (string)
- "steps": chronological array of actionable steps or rules (array of strings)
- "deadlines": array of objects [{"date": string, "description": string}]
- "required_documents": array of documents/certificates required (array of strings)
- "risks": array of critical risks, warnings, penalties, or consequences (array of strings)
All values in English."""

resp = client.chat.completions.create(
    model="qwen/qwen3.6-27b",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"DOCUMENT CONTENT:\n{doc_text[:12000]}"}
    ],
    max_tokens=4096,
    temperature=0.1
)

content = resp.choices[0].message.content
parsed = clean_json_response(content)
assert parsed is not None
normalized = normalize_analysis_dict(parsed)
print("Analysis Success!")
print("Doc Type:", normalized["doc_type"])
print("Summary:", normalized["summary"])
print("Steps:", normalized["steps"])
print("Deadlines:", normalized["deadlines"])
print("Risks:", normalized["risks"])
