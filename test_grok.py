import unittest
import os
from logic.grok_calls import general_answer
from streamlit.testing.v1 import AppTest

class TestGrokIntegration(unittest.TestCase):
    def test_01_grok_missing_key_behavior(self):
        print("\n--- Testing Grok Missing API Key Behavior ---")
        orig_key = os.environ.get("XAI_API_KEY")
        if "XAI_API_KEY" in os.environ:
            del os.environ["XAI_API_KEY"]
            
        ans = general_answer("What documents are needed for PAN card?", language="English")
        self.assertEqual(ans, "Search is not configured")
        print("[OK] Returns 'Search is not configured' when XAI_API_KEY is not set")
        
        if orig_key:
            os.environ["XAI_API_KEY"] = orig_key

    def test_02_ask_page_navigation(self):
        print("\n--- Testing Ask Page Navigation ---")
        at = AppTest.from_file("app.py", default_timeout=15)
        at.run()
        
        # Login
        at.text_input[0].input("Kavya Nair")
        at.button[0].click().run()
        self.assertEqual(at.session_state["page"], "home")
        
        # Click Ask AI icon button on Home
        btn_ask = [b for b in at.button if "Ask AI" in (b.label or "") or (b.key and "btn_home_ask_icon" in b.key)]
        self.assertTrue(len(btn_ask) > 0)
        btn_ask[0].click().run()
        
        self.assertEqual(at.session_state["page"], "ask")
        print("[OK] Home 'Ask AI' icon navigated to pages/ask.py cleanly")
        
        # Click Back to Home
        btn_back = [b for b in at.button if "Back to Home" in (b.label or "")]
        self.assertTrue(len(btn_back) > 0)
        btn_back[0].click().run()
        self.assertEqual(at.session_state["page"], "home")
        print("[OK] Ask page Back to Home returned to home screen without affecting state")

if __name__ == "__main__":
    unittest.main()
