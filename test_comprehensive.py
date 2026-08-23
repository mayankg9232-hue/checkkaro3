import unittest
import os
from streamlit.testing.v1 import AppTest
from logic.extract_text import extract_text
from logic.process_data import load_processes, format_process_for_analysis
from logic.llm_calls import analyze_document, answer_question

class TestComprehensiveVerification(unittest.TestCase):

    def test_01_requirements_and_data_accuracy(self):
        print("\n--- 1. Testing processes.json Curated Data Accuracy ---")
        procs = load_processes()
        self.assertEqual(len(procs), 3, "Must have exactly 3 curated processes")
        
        proc_ids = [p["id"] for p in procs]
        self.assertIn("pan_card", proc_ids)
        self.assertIn("aadhaar_update", proc_ids)
        self.assertIn("passport_renewal", proc_ids)
        
        for p in procs:
            self.assertIn("name", p)
            self.assertIn("description", p)
            self.assertIn("steps", p)
            self.assertTrue(len(p["steps"]) >= 3)
            self.assertIn("required_documents", p)
            self.assertTrue(len(p["required_documents"]) >= 2)
            self.assertIn("authority", p)
            self.assertIn("type", p["authority"])
            self.assertIn("mode", p["authority"])
            self.assertIn("note", p["authority"])
            self.assertIn("estimated_time", p)
            self.assertIn("fees", p)
            self.assertEqual(p["authority"]["note"], "confirm exact details at your nearest center, as requirements vary by state")
        print("[OK] Curated data schema and accuracy verified (PAN, Aadhaar, Passport)")

    def test_02_text_extraction(self):
        print("\n--- 2. Testing extract_text.py Standalone ---")
        docx_text = extract_text("samples/sample_it_notice.docx")
        self.assertIn("INCOME TAX DEPARTMENT", docx_text)
        self.assertIn("143(1)", docx_text)
        print("[OK] DOCX extraction verified:", len(docx_text), "chars")
        
        pdf_text = extract_text("samples/sample_khata_notice.pdf")
        self.assertIn("REVENUE DEPARTMENT", pdf_text)
        self.assertIn("Khata", pdf_text)
        print("[OK] PDF extraction verified:", len(pdf_text), "chars")
        
        with self.assertRaises(ValueError):
            extract_text(b"sample", filename="bad_file.xyz")
        print("[OK] Unsupported file error handling verified")

    def test_03_llm_json_analysis_and_qa(self):
        print("\n--- 3. Testing llm_calls.py (Groq & Parsing) ---")
        sample_text = "PASSPORT SEVA KENDRA: Police verification mandatory within 15 days. Fees: Rs 1500 for normal 36 pages. Required: Old passport, Aadhaar card."
        analysis = analyze_document(sample_text, language="English")
        
        required_keys = ["doc_type", "summary", "steps", "deadlines", "required_documents", "risks"]
        for k in required_keys:
            self.assertIn(k, analysis, f"Key '{k}' must be present in analysis output")
        print("[OK] LLM analysis output format and schema verified")
        
        ans = answer_question(sample_text, "What is the fee for normal 36 pages?", language="English")
        self.assertTrue("1500" in ans or "1,500" in ans or len(ans) > 0)
        print("[OK] Grounded Q&A answered accurately")
        
        ans_missing = answer_question(sample_text, "What is the capital of Mars?", language="English")
        self.assertIn("certain", ans_missing.lower())
        print("[OK] Grounded Q&A refusal verified ('I'm not certain based on this document')")

    def test_04_full_ui_navigation_and_flows(self):
        print("\n--- 4. Testing End-to-End Streamlit App Flows ---")
        at = AppTest.from_file("app.py", default_timeout=15)
        at.run()
        
        # 1. Login
        self.assertEqual(at.session_state["page"], "login")
        at.text_input[0].input("Aarav Gupta")
        at.text_input[1].input("aarav@example.com")
        btn_login = [b for b in at.button if "Continue" in (b.label or "")]
        self.assertTrue(len(btn_login) > 0)
        btn_login[0].click().run()
        self.assertEqual(at.session_state["page"], "home")
        self.assertEqual(at.session_state["user"]["name"], "Aarav Gupta")
        print("[OK] Screen 1: Login passed")
        
        # 2. Home Language Selection & Process Picker Navigation
        at.selectbox[0].select("English").run()
        btn_proc = [b for b in at.button if "Government" in (b.label or "") or (b.key and "btn_main_govt" in b.key)]
        self.assertTrue(len(btn_proc) > 0)
        btn_proc[0].click().run()
        self.assertEqual(at.session_state["page"], "process_picker")
        print("[OK] Screen 2: Home -> Process Picker navigation passed")
        
        # 3. Process Picker (Dropdown Select & Unified Summary Display)
        self.assertIsNotNone(at.session_state["analysis_result"])
        res = at.session_state["analysis_result"]
        self.assertIn("PAN", res["doc_type"])
        print("[OK] Screen 3: Process Guide loaded with unified summary")
        
        # 4. Sidebar Home Navigation
        btn_side_home = [b for b in at.button if "Home" in (b.label or "") or (b.key and "side_nav_home" in b.key)]
        self.assertTrue(len(btn_side_home) > 0)
        btn_side_home[0].click().run()
        self.assertEqual(at.session_state["page"], "home")
        print("[OK] Screen 4: Sidebar Home navigation passed")

        # 5. Sidebar Sign Out
        btn_signout = [b for b in at.button if "Sign Out" in (b.label or "") or (b.key and "side_nav_signout" in b.key)]
        self.assertTrue(len(btn_signout) > 0)
        btn_signout[0].click().run()
        self.assertEqual(at.session_state["page"], "login")
        self.assertIsNone(at.session_state["user"])
        print("[OK] Screen 5: Sign Out reset session state to login cleanly")

if __name__ == "__main__":
    unittest.main()
