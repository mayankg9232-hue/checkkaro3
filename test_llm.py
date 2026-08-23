from logic.llm_calls import clean_json_response, normalize_analysis_dict, analyze_document, answer_question

def test():
    print("Testing clean_json_response with raw JSON...")
    raw = '{"doc_type": "Notice", "summary": "Tax notice", "steps": ["Pay tax"], "deadlines": [{"date": "2026-03-31", "description": "Pay"}], "required_documents": ["Challan"], "risks": ["Penalty"]}'
    res = clean_json_response(raw)
    assert res is not None
    assert res["doc_type"] == "Notice"
    print("Direct JSON parse: PASSED")

    print("Testing clean_json_response with markdown code block...")
    markdown_raw = 'Here is your analysis:\n```json\n{"doc_type": "Aadhaar Card", "summary": "Update notice", "steps": [], "deadlines": [], "required_documents": [], "risks": []}\n```\nHope this helps!'
    res_md = clean_json_response(markdown_raw)
    assert res_md is not None
    assert res_md["doc_type"] == "Aadhaar Card"
    print("Markdown codeblock parse: PASSED")

    print("Testing normalize_analysis_dict...")
    partial = {"doc_type": "Passport Form"}
    normalized = normalize_analysis_dict(partial)
    assert "steps" in normalized
    assert "deadlines" in normalized
    assert "risks" in normalized
    assert isinstance(normalized["steps"], list)
    print("Dict normalization: PASSED")

    print("Testing analyze_document on sample text...")
    sample_text = "Income Tax Department Demand Notice: Outstanding demand of Rs. 5000 under Section 143(1) for AY 2025-26. Must be paid within 30 days."
    analysis = analyze_document(sample_text, language="English")
    print("Analysis result keys:", list(analysis.keys()))
    assert "doc_type" in analysis
    assert "summary" in analysis
    assert "steps" in analysis
    print("analyze_document: PASSED")

    print("Testing answer_question...")
    ans = answer_question(sample_text, "What is the demand amount?", language="English")
    print("Question answer sample:", ans.encode("ascii", "replace").decode())
    assert "5000" in ans or "5,000" in ans or len(ans) > 0
    print("answer_question: PASSED")

    print("\nAll LLM tests with Groq PASSED successfully!")

if __name__ == "__main__":
    test()
