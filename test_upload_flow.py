import unittest
from streamlit.testing.v1 import AppTest
from logic.extract_text import get_text
from logic.llm_calls import analyze_document, answer_question

class TestDedicatedUploadFlow(unittest.TestCase):
    def test_upload_screen_flow(self):
        print("\n--- Testing Dedicated Upload Screen Flow ---")
        at = AppTest.from_file("app.py", default_timeout=15)
        at.run()
        
        # 1. Login
        at.text_input[0].input("Priya Sharma")
        btn_login = [b for b in at.button if "Continue" in (b.label or "")]
        btn_login[0].click().run()
        self.assertEqual(at.session_state["page"], "home")
        
        # 2. Click Upload Document Category Button
        btn_upload = [b for b in at.button if "Upload" in (b.label or "") or (b.key and "cat_btn_upload" in b.key)]
        self.assertTrue(len(btn_upload) > 0)
        btn_upload[0].click().run()
        self.assertEqual(at.session_state["page"], "upload")
        print("[OK] Routed to dedicated Upload screen (page='upload')")

if __name__ == "__main__":
    unittest.main()
