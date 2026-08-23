import unittest
from streamlit.testing.v1 import AppTest
from logic.process_data import load_processes, get_process_by_id

class TestBankingSection(unittest.TestCase):

    def test_01_banking_data_structure(self):
        print("\n--- 1. Testing Banking Processes Data Structure ---")
        procs = load_processes(category="banking", language="English")
        self.assertEqual(len(procs), 4, "Should contain exactly 4 curated banking processes")
        
        proc_ids = [p["id"] for p in procs]
        self.assertIn("loan_documentation", proc_ids)
        self.assertIn("kyc_account_opening", proc_ids)
        self.assertIn("update_account_details", proc_ids)
        self.assertIn("account_transfer", proc_ids)

        for p in procs:
            self.assertTrue(len(p["name"]) > 0)
            self.assertTrue(len(p["description"]) > 0)
            self.assertTrue(len(p["steps"]) >= 4)
            self.assertTrue(len(p["required_documents"]) >= 3)
            self.assertIn("type", p["authority"])
        print("[OK] All 4 Banking topics verified with complete schema")

    def test_02_banking_multilingual_localization(self):
        print("\n--- 2. Testing Banking Multilingual Localization ---")
        procs_hi = load_processes(category="banking", language="Hindi")
        self.assertIn("बैंक ऋण", procs_hi[0]["name"])
        self.assertIn("केवाईसी", procs_hi[1]["name"])
        self.assertIn("विवरण अपडेट", procs_hi[2]["name"])
        self.assertIn("शाखा स्थानांतरण", procs_hi[3]["name"])

        procs_kn = load_processes(category="banking", language="Kannada")
        self.assertIn("ಸಾಲ", procs_kn[0]["name"])
        self.assertIn("ಕೆವೈಸಿ", procs_kn[1]["name"])
        self.assertIn("ವಿವರಗಳನ್ನು ನವೀಕರಿಸುವುದು", procs_kn[2]["name"])
        self.assertIn("ಶಾಖೆ ವರ್ಗಾವಣೆ", procs_kn[3]["name"])
        print("[OK] Banking processes localized across English, Hindi, and Kannada")

    def test_03_banking_navigation_flow(self):
        print("\n--- 3. Testing Home -> Banking Flow ---")
        at = AppTest.from_file("app.py", default_timeout=15)
        at.run()

        # Login
        at.text_input[0].input("Kavita Rao")
        at.button[0].click().run()
        self.assertEqual(at.session_state["page"], "home")

        # Click Banking Services
        btn_banking = [b for b in at.button if "Banking" in (b.label or "") or "बैंकिंग" in (b.label or "")]
        self.assertTrue(len(btn_banking) > 0)
        btn_banking[0].click().run()

        self.assertEqual(at.session_state["page"], "process_picker")
        self.assertEqual(at.session_state["guide_category"], "banking")

        # Find banking guide selector
        guide_selectors = [s for s in at.selectbox if any("Bank" in opt or "Loan" in opt or "Account" in opt for opt in s.options)]
        self.assertTrue(len(guide_selectors) > 0)
        selector = guide_selectors[0]
        
        # Select "Updating Bank Account Details"
        update_opt = [o for o in selector.options if "Updating" in o or "Details" in o][0]
        selector.select(update_opt).run()

        self.assertEqual(at.session_state["selected_process_id"], "update_account_details")
        print("[OK] Banking section loaded and 'Update Account Details' displayed successfully")

if __name__ == "__main__":
    unittest.main()
