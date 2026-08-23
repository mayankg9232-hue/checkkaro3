import unittest
import os
from streamlit.testing.v1 import AppTest
from logic.extract_text import extract_text
from logic.process_data import load_processes, format_process_for_analysis
from logic.llm_calls import analyze_document, answer_question

class TestDocAssistantApp(unittest.TestCase):

    def test_01_login_and_home_navigation(self):
        print("\n--- Testing Login & Home Navigation ---")
        at = AppTest.from_file("app.py", default_timeout=15)
        at.run()
        self.assertEqual(at.session_state["page"], "login")
        
        # Fill in login form
        at.text_input[0].input("Ramesh Kumar")
        at.text_input[1].input("ramesh@example.com")
        at.button[0].click().run()
        
        self.assertEqual(at.session_state["page"], "home")
        self.assertEqual(at.session_state["user"]["name"], "Ramesh Kumar")
        print("[OK] Login successfully transitioned to Home screen")

    def test_02_curated_process_flow(self):
        print("\n--- Testing Curated Process Picker & Dashboard Flow ---")
        at = AppTest.from_file("app.py", default_timeout=15)
        at.run()
        
        # Simulate logged in user
        at.session_state["user"] = {"name": "Priya Sharma", "email": "priya@example.com"}
        at.session_state["page"] = "home"
        at.run()
        
        # Navigate to Process Picker
        btn_proc = [b for b in at.button if "Government" in (b.label or "") or "Process" in (b.label or "") or (b.key and "btn_choose_process" in b.key)]
        self.assertTrue(len(btn_proc) > 0)
        btn_proc[0].click().run()
        
        self.assertEqual(at.session_state["page"], "process_picker")
        print("[OK] Navigated to Process Picker")
        
        # Select first process guide (PAN Card)
        view_guide_btns = [b for b in at.button if "View Guide" in (b.label or "")]
        self.assertTrue(len(view_guide_btns) >= 3)
        view_guide_btns[0].click().run()
        
        self.assertEqual(at.session_state["page"], "dashboard")
        self.assertIsNotNone(at.session_state["analysis_result"])
        result = at.session_state["analysis_result"]
        self.assertIn("PAN", result["doc_type"])
        self.assertTrue(len(result["steps"]) > 0)
        self.assertTrue(len(result["required_documents"]) > 0)
        self.assertIn("authority", result)
        print("[OK] Loaded PAN Card Guide into Dashboard with correct schema")
        
        # Test checkbox toggle in Steps Tab
        if len(at.checkbox) > 0:
            at.checkbox[0].check().run()
            self.assertTrue(at.session_state["step_progress"][list(at.session_state["step_progress"].keys())[0]])
            print("[OK] Checkbox interaction persisted in step_progress state")

    def test_03_document_extraction_and_analysis_flow(self):
        print("\n--- Testing Document Upload & Analysis Pipeline ---")
        # 1. DOCX Extraction & Analysis
        docx_path = "samples/sample_it_notice.docx"
        text_docx = extract_text(docx_path)
        self.assertIn("INCOME TAX DEPARTMENT", text_docx)
        print("[OK] DOCX text extracted:", len(text_docx), "chars")
        
        analysis_docx = analyze_document(text_docx, language="English")
        self.assertIn("doc_type", analysis_docx)
        self.assertIn("summary", analysis_docx)
        self.assertIn("steps", analysis_docx)
        self.assertIn("deadlines", analysis_docx)
        self.assertIn("required_documents", analysis_docx)
        self.assertIn("risks", analysis_docx)
        print("[OK] Document analysis generated valid schema keys")
        
        # 2. PDF Extraction & Analysis
        pdf_path = "samples/sample_khata_notice.pdf"
        text_pdf = extract_text(pdf_path)
        self.assertIn("REVENUE DEPARTMENT", text_pdf)
        print("[OK] PDF text extracted:", len(text_pdf), "chars")
        
        # 3. Test Grounded Q&A
        q = "What is the tax amount payable?"
        ans = answer_question(text_docx, q, language="English")
        print(f"[OK] Q&A Answer received: {ans.encode('ascii', 'replace').decode()[:80]}...")
        self.assertTrue(len(ans) > 0)
        
        # 4. Test Unknown Grounded Q&A
        q_unknown = "What is the secret recipe for chocolate cake?"
        ans_unknown = answer_question(text_docx, q_unknown, language="English")
        print(f"[OK] Q&A Unknown Query Response: {ans_unknown.encode('ascii', 'replace').decode()}")
        
    def test_04_sidebar_start_over(self):
        print("\n--- Testing Start Over & Reset ---")
        at = AppTest.from_file("app.py", default_timeout=15)
        at.run()
        
        at.session_state["user"] = {"name": "Test User", "email": "test@test.com"}
        at.session_state["page"] = "dashboard"
        at.session_state["analysis_result"] = {"doc_type": "Test", "summary": "Summary", "steps": []}
        at.session_state["chat_history"] = [{"role": "user", "content": "Hi"}]
        at.run()
        
        # Find Start Over button
        btn_start_over = [b for b in at.button if "Start Over" in (b.label or "")]
        self.assertTrue(len(btn_start_over) > 0)
        btn_start_over[0].click().run()
        
        self.assertEqual(at.session_state["page"], "home")
        self.assertIsNone(at.session_state["analysis_result"])
        self.assertEqual(len(at.session_state["chat_history"]), 0)
        self.assertEqual(at.session_state["user"]["name"], "Test User")
        print("[OK] Start Over reset state cleanly back to Home")

if __name__ == "__main__":
    unittest.main()
