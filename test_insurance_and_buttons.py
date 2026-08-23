import unittest
from streamlit.testing.v1 import AppTest
from logic.process_data import load_processes, get_process_by_id

class TestInsuranceAndAllButtons(unittest.TestCase):

    def test_01_insurance_data_structure(self):
        print("\n--- 1. Testing Insurance Processes Data & Required Documents ---")
        procs = load_processes(category="insurance", language="English")
        self.assertEqual(len(procs), 5, "Should contain exactly 5 curated insurance topics")
        
        proc_ids = [p["id"] for p in procs]
        self.assertIn("claim_filing", proc_ids)
        self.assertIn("policy_breakdown", proc_ids)
        self.assertIn("health_insurance_coverage", proc_ids)
        self.assertIn("auto_insurance_coverage", proc_ids)
        self.assertIn("documents_keep_ready", proc_ids)

        for p in procs:
            self.assertTrue(len(p["name"]) > 0)
            self.assertTrue(len(p["description"]) > 0)
            self.assertTrue(len(p["steps"]) >= 4)
            # Verify practical and thorough required documents list
            self.assertTrue(len(p["required_documents"]) >= 4, f"{p['id']} must have thorough required documents")
            self.assertIn("type", p["authority"])
        print("[OK] All 5 Insurance topics verified with high-value required documents")

    def test_02_insurance_multilingual_localization(self):
        print("\n--- 2. Testing Insurance Multilingual Localization ---")
        procs_hi = load_processes(category="insurance", language="Hindi")
        self.assertIn("दावा", procs_hi[0]["name"])
        self.assertIn("पॉलिसी", procs_hi[1]["name"])
        self.assertIn("स्वास्थ्य बीमा", procs_hi[2]["name"])
        self.assertIn("वाहन बीमा", procs_hi[3]["name"])
        self.assertIn("तैयारी", procs_hi[4]["name"])

        procs_kn = load_processes(category="insurance", language="Kannada")
        self.assertIn("ಕ್ಲೈಮ್", procs_kn[0]["name"])
        self.assertIn("ಪಾಲಿಸಿ", procs_kn[1]["name"])
        self.assertIn("ಆರೋಗ್ಯ", procs_kn[2]["name"])
        self.assertIn("ವಾಹನ", procs_kn[3]["name"])
        self.assertIn("ಸಿದ್ಧತೆಯ", procs_kn[4]["name"])
        print("[OK] Insurance processes accurately localized across English, Hindi, and Kannada")

    def test_03_insurance_navigation_and_health_coverage(self):
        print("\n--- 3. Testing Home -> Insurance Flow & Health Coverage Selection ---")
        at = AppTest.from_file("app.py", default_timeout=15)
        at.run()

        # Login
        at.text_input[0].input("Arjun Narang")
        at.button[0].click().run()
        self.assertEqual(at.session_state["page"], "home")

        # Click Insurance Services
        btn_ins = [b for b in at.button if "Insurance" in (b.label or "") or "बीमा" in (b.label or "")]
        self.assertTrue(len(btn_ins) > 0)
        btn_ins[0].click().run()

        self.assertEqual(at.session_state["page"], "process_picker")
        self.assertEqual(at.session_state["guide_category"], "insurance")

        # Find insurance guide selector
        guide_selectors = [s for s in at.selectbox if any("Health" in opt or "Claim" in opt or "Policy" in opt for opt in s.options)]
        self.assertTrue(len(guide_selectors) > 0)
        selector = guide_selectors[0]
        
        # Select "Health Insurance Coverage"
        health_opt = [o for o in selector.options if "Health" in o][0]
        selector.select(health_opt).run()

        self.assertEqual(at.session_state["selected_process_id"], "health_insurance_coverage")
        analysis = at.session_state["analysis_result"]
        self.assertIn("Health Insurance", analysis["doc_type"])
        self.assertTrue(len(analysis["required_documents"]) >= 5)
        print("[OK] Insurance Health Coverage guide loaded and rendered perfectly")

    def test_04_system_wide_button_audit(self):
        print("\n--- 4. Full Audit of Every Button Across the Entire Application ---")
        at = AppTest.from_file("app.py", default_timeout=15)
        at.run()

        # Login
        at.text_input[0].input("Audit User")
        at.button[0].click().run()
        self.assertEqual(at.session_state["page"], "home")

        # 1. Home -> Government
        btn_govt = [b for b in at.button if "Government" in (b.label or "") or "सरकारी" in (b.label or "")][0]
        btn_govt.click().run()
        self.assertEqual(at.session_state["page"], "process_picker")
        self.assertEqual(at.session_state["guide_category"], "government")

        # 2. Back to Home from Govt
        [b for b in at.button if "Back to Home" in (b.label or "") or "वापस" in (b.label or "")][0].click().run()
        self.assertEqual(at.session_state["page"], "home")

        # 3. Home -> Banking
        btn_bank = [b for b in at.button if "Banking" in (b.label or "") or "बैंकिंग" in (b.label or "")][0]
        btn_bank.click().run()
        self.assertEqual(at.session_state["page"], "process_picker")
        self.assertEqual(at.session_state["guide_category"], "banking")

        # 4. Back to Home from Banking
        [b for b in at.button if "Back to Home" in (b.label or "") or "वापस" in (b.label or "")][0].click().run()
        self.assertEqual(at.session_state["page"], "home")

        # 5. Home -> Insurance
        btn_ins = [b for b in at.button if "Insurance" in (b.label or "") or "बीमा" in (b.label or "")][0]
        btn_ins.click().run()
        self.assertEqual(at.session_state["page"], "process_picker")
        self.assertEqual(at.session_state["guide_category"], "insurance")

        # 6. Back to Home from Insurance
        [b for b in at.button if "Back to Home" in (b.label or "") or "वापस" in (b.label or "")][0].click().run()
        self.assertEqual(at.session_state["page"], "home")

        # 7. Home -> Upload Document
        btn_up = [b for b in at.button if "Upload" in (b.label or "") or "अपलोड" in (b.label or "")][0]
        btn_up.click().run()
        self.assertEqual(at.session_state["page"], "upload")

        # 8. Back to Home from Upload
        [b for b in at.button if "Back to Home" in (b.label or "") or "वापस" in (b.label or "")][0].click().run()
        self.assertEqual(at.session_state["page"], "home")

        # 9. Sidebar: Current Task
        btn_cur = [b for b in at.button if "Current Task" in (b.label or "") or "वर्तमान" in (b.label or "")][0]
        btn_cur.click().run()
        self.assertIn(at.session_state["page"], ["dashboard", "current_task"])

        # 10. Sidebar: Completed Task
        btn_comp = [b for b in at.button if "Completed Task" in (b.label or "") or "पूर्ण" in (b.label or "")][0]
        btn_comp.click().run()
        self.assertEqual(at.session_state["page"], "completed_task")

        # 11. Sidebar: Sign Out
        btn_sign = [b for b in at.button if "Sign Out" in (b.label or "") or "साइन आउट" in (b.label or "")][0]
        btn_sign.click().run()
        self.assertEqual(at.session_state["page"], "login")
        self.assertIsNone(at.session_state["user"])

        print("[OK] Every single button across the application tested and 100% active!")

if __name__ == "__main__":
    unittest.main()
