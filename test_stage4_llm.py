import sys
import json
from logic.llm_calls import analyze_document, answer_question

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sample_input_text = """
INCOME TAX DEPARTMENT - GOVERNMENT OF INDIA
Intimation under Section 143(1) of the Income-tax Act, 1961
Assessment Year: 2025-26 | PAN: ABCDE1234F | Notice Date: 15-Aug-2026

Dear Taxpayer,
Your return of income for AY 2025-26 has been processed. Upon processing, there is an outstanding net demand payable of Rs. 4,500.
You must pay this amount within 30 days of receipt via Challan ITNS 280 / e-Pay Tax.
Failure to pay within 30 days will attract additional interest under Section 220(2) at 1% per month.
Required documents: Form 16 / TDS certificates, Bank statement showing tax deduction.
"""

def test_llm():
    print("==================================================")
    print("1. Testing analyze_document(text, language='English')")
    print("==================================================")
    analysis = analyze_document(sample_input_text, language="English")
    print(json.dumps(analysis, indent=2, ensure_ascii=False))
    
    # Assertions
    assert "doc_type" in analysis, "doc_type field is missing"
    assert "summary" in analysis, "summary field is missing"
    assert "steps" in analysis, "steps field is missing"
    assert "deadlines" in analysis, "deadlines field is missing"
    assert "required_documents" in analysis, "required_documents field is missing"
    assert "risks" in analysis, "risks field is missing"
    print("\n[OK] analyze_document returned valid structured JSON!")

    print("\n==================================================")
    print("2. Testing answer_question (Valid Query in Document)")
    print("==================================================")
    q1 = "What is the outstanding tax amount payable and what is the deadline?"
    ans1 = answer_question(sample_input_text, q1, language="English")
    print(f"Question: {q1}")
    print(f"Answer: {ans1}")

    print("\n==================================================")
    print("3. Testing answer_question (Missing Query / Unsure Refusal)")
    print("==================================================")
    q2 = "Who is the Prime Minister of Australia?"
    ans2 = answer_question(sample_input_text, q2, language="English")
    print(f"Question: {q2}")
    print(f"Answer: {ans2}")
    assert "not certain based on this document" in ans2.lower() or "not certain" in ans2.lower()
    print("\n[OK] answer_question returned refusal phrase accurately!")

if __name__ == "__main__":
    test_llm()
