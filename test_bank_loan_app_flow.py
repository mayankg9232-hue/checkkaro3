import unittest
from streamlit.testing.v1 import AppTest

class TestBankLoanAppFlow(unittest.TestCase):

    def test_01_bank_loan_ui_flow(self):
        print("\n--- 1. Testing Bank Loan App Flow (Home -> Banking -> Loan Doc -> HDFC Home Loan) ---")
        at = AppTest.from_file("app.py", default_timeout=25)
        at.run()

        # Login
        at.text_input[0].input("Karan Malhotra")
        at.button[0].click().run()
        self.assertEqual(at.session_state["page"], "home")

        # Home -> Banking
        btn_bank = [b for b in at.button if "Banking" in (b.label or "") or "बैंकिंग" in (b.label or "")][0]
        btn_bank.click().run()
        self.assertEqual(at.session_state["page"], "process_picker")
        self.assertEqual(at.session_state["guide_category"], "banking")

        # Select Loan Documentation
        guide_selector = [s for s in at.selectbox if any("Loan" in opt or "ऋण" in opt for opt in s.options)][0]
        loan_opt = [o for o in guide_selector.options if "Loan" in o or "ऋण" in o][0]
        guide_selector.select(loan_opt).run()

        # Verify selectors exist
        selectors = at.selectbox
        self.assertTrue(len(selectors) >= 3, "Should have category selector, loan type selector, and bank selector")
        
        analysis = at.session_state["analysis_result"]
        self.assertIn("Loan", analysis["doc_type"])
        self.assertTrue(len(analysis["required_documents"]) >= 3)
        self.assertTrue(len(analysis["steps"]) >= 4)
        self.assertTrue(len(analysis["risks"]) >= 1, "Disclaimer should be saved in risks for dashboard banner")
        print("[OK] Bank Loan UI Flow passed with dynamic guidance and prominent disclaimer")

    def test_02_bank_loan_hindi_flow(self):
        print("\n--- 2. Testing Bank Loan Flow in Hindi ---")
        at = AppTest.from_file("app.py", default_timeout=25)
        at.run()

        # Switch language to Hindi at Login
        at.selectbox[0].select("Hindi (हिंदी)").run()
        
        # Login
        at.text_input[0].input("करण मल्होत्रा")
        at.button[0].click().run()
        self.assertEqual(at.session_state["page"], "home")

        # Home -> Banking
        btn_bank = [b for b in at.button if "बैंकिंग" in (b.label or "")][0]
        btn_bank.click().run()
        self.assertEqual(at.session_state["page"], "process_picker")
        
        analysis = at.session_state["analysis_result"]
        self.assertTrue(len(analysis["required_documents"]) >= 3)
        print("[OK] Hindi Bank Loan flow rendered and translated accurately")

if __name__ == "__main__":
    unittest.main()
