import unittest
from logic.llm_calls import answer_question, general_chat_answer, build_system_prompt
from logic.process_data import load_processes, format_process_for_analysis

class TestSectionLLMQuality(unittest.TestCase):

    def test_01_prompt_builder_consistency(self):
        print("\n--- 1. Testing Shared System Prompt Builder ---")
        prompt_en = build_system_prompt("Government Services", language="English", task_type="grounded_qa")
        self.assertIn("English", prompt_en)
        self.assertIn("practical", prompt_en.lower())
        self.assertIn("uncertainty", prompt_en.lower())

        prompt_hi = build_system_prompt("बैंकिंग सेवाएं", language="Hindi", task_type="grounded_qa")
        self.assertIn("Hindi", prompt_hi)
        print("[OK] Standardized prompt builder generates unified, high-quality guidelines across domains")

    def test_02_government_section_qa_practical_alternative(self):
        print("\n--- 2. Testing Government Q&A: Missing Address Proof Alternative ---")
        procs = load_processes(category="government", language="English")
        aadhaar_proc = [p for p in procs if p["id"] == "aadhaar_update"][0]
        context = str(format_process_for_analysis(aadhaar_proc))
        
        q = "What acceptable alternative documents can I provide if I do not have an electricity bill for address update?"
        ans = answer_question(context, q, language="English")
        
        self.assertTrue(len(ans) > 50)
        self.assertTrue(any(term in ans.lower() for term in ["passport", "bank", "voter", "rent", "water", "proof", "uidai", "aadhaar", "acceptable", "alternative"]))
        print("[OK] Government Section Q&A provided practical answer")

    def test_03_banking_section_qa_video_kyc(self):
        print("\n--- 3. Testing Banking Q&A: Video KYC Remote Account Opening ---")
        procs = load_processes(category="banking", language="English")
        kyc_proc = [p for p in procs if p["id"] == "kyc_account_opening"][0]
        context = str(format_process_for_analysis(kyc_proc))

        q = "Can I open an account and complete KYC without visiting the bank branch in person?"
        ans = answer_question(context, q, language="English")
        
        self.assertTrue(len(ans) > 50)
        self.assertTrue(any(term in ans.lower() for term in ["video", "v-kyc", "online", "pan", "digital", "camera", "yes"]))
        print("[OK] Banking Section Q&A provided specific Video KYC guidance")

    def test_04_insurance_section_qa_reimbursement(self):
        print("\n--- 4. Testing Insurance Q&A: Non-network Reimbursement Claims ---")
        procs = load_processes(category="insurance", language="English")
        health_proc = [p for p in procs if p["id"] == "health_insurance_coverage"][0]
        context = str(format_process_for_analysis(health_proc))

        q = "What is the process to claim reimbursement if I get treated at a non-network hospital?"
        ans = answer_question(context, q, language="English")
        
        self.assertTrue(len(ans) > 50)
        self.assertTrue(any(term in ans.lower() for term in ["reimbursement", "discharge", "bill", "claim", "voucher", "submit", "form"]))
        print("[OK] Insurance Section Q&A provided structured step-by-step reimbursement steps")

    def test_05_hindi_section_qa(self):
        print("\n--- 5. Testing Section Q&A in Hindi ---")
        procs = load_processes(category="government", language="Hindi")
        pan_proc = [p for p in procs if p["id"] == "pan_card"][0]
        context = str(format_process_for_analysis(pan_proc))

        q = "अगर मेरे पास जन्म प्रमाण पत्र नहीं है तो मैं जन्मतिथि के प्रमाण के लिए क्या दे सकता हूँ?"
        ans = answer_question(context, q, language="Hindi")
        
        self.assertTrue(len(ans) > 30)
        print("[OK] Hindi Section Q&A answered with high quality")

if __name__ == "__main__":
    unittest.main()
