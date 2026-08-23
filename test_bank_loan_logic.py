import unittest
from logic.llm_calls import bank_loan_info
from logic.process_data import load_processes

class TestBankLoanGuidance(unittest.TestCase):

    def test_01_banking_json_data(self):
        print("\n--- 1. Testing Banking Processes Data Structure ---")
        procs = load_processes(category="banking", language="English")
        loan_proc = [p for p in procs if p["id"] == "loan_documentation"][0]
        
        self.assertIn("loan_types", loan_proc)
        self.assertIn("banks", loan_proc)
        self.assertEqual(len(loan_proc["loan_types"]), 5)
        self.assertEqual(len(loan_proc["banks"]), 12)
        self.assertIn("Home Loan", loan_proc["loan_types"])
        self.assertIn("HDFC Bank", loan_proc["banks"])
        self.assertIn("State Bank of India", loan_proc["banks"])
        print("[OK] Banking JSON data has all 5 loan types and 12 banks")

    def test_02_bank_loan_info_hdfc_home_loan(self):
        print("\n--- 2. Testing bank_loan_info: HDFC Bank + Home Loan (English) ---")
        res = bank_loan_info("HDFC Bank", "Home Loan", language="English")
        
        self.assertIn("overview", res)
        self.assertIn("typical_documents", res)
        self.assertIn("general_process", res)
        self.assertIn("disclaimer", res)
        self.assertTrue(len(res["typical_documents"]) >= 3)
        self.assertTrue(len(res["general_process"]) >= 4)
        
        # Verify disclaimer mentions variability
        self.assertTrue(any(term in res["disclaimer"].lower() for term in ["vary", "varies", "confirm", "website", "branch"]))
        print("[OK] HDFC Bank Home Loan guidance generated accurately with clear disclaimer")

    def test_03_multiple_bank_and_loan_combinations(self):
        print("\n--- 3. Testing 3 different Bank + Loan Type combinations ---")
        combos = [
            ("State Bank of India", "Education Loan"),
            ("ICICI Bank", "Personal Loan"),
            ("Axis Bank", "Business Loan")
        ]
        for bank, ltype in combos:
            res = bank_loan_info(bank, ltype, language="English")
            self.assertIn("overview", res)
            self.assertTrue(len(res["typical_documents"]) >= 3)
            self.assertTrue(len(res["general_process"]) >= 3)
            self.assertIn("disclaimer", res)
            print(f"  [OK] {bank} + {ltype} passed")

    def test_04_bank_loan_info_hindi(self):
        print("\n--- 4. Testing bank_loan_info in Hindi ---")
        res = bank_loan_info("State Bank of India", "Home Loan", language="Hindi")
        self.assertIn("overview", res)
        self.assertIn("typical_documents", res)
        self.assertIn("disclaimer", res)
        print("[OK] Hindi bank loan guidance generated successfully")

if __name__ == "__main__":
    unittest.main()
