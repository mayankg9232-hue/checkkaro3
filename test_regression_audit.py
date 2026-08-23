import unittest
from streamlit.testing.v1 import AppTest

class TestRegressionAudit(unittest.TestCase):

    def test_01_full_clickthrough_regression(self):
        print("\n--- 1. Testing Full Click-Through Single Session Regression ---")
        at = AppTest.from_file("app.py", default_timeout=15)
        at.run()

        # Step 1: Login
        self.assertEqual(at.session_state["page"], "login")
        at.text_input[0].input("Deepak Verma")
        at.button[0].click().run()
        self.assertEqual(at.session_state["page"], "home")
        self.assertEqual(at.session_state["user"]["name"], "Deepak Verma")
        print("[OK] Step 1: Login passed")

        # Step 2: Home -> Government Services
        btn_govt = [b for b in at.button if "Government" in (b.label or "") or "सरकारी" in (b.label or "")][0]
        btn_govt.click().run()
        self.assertEqual(at.session_state["page"], "process_picker")
        self.assertEqual(at.session_state["guide_category"], "government")
        print("[OK] Step 2: Home -> Government Process Picker passed")

        # Step 3: Back to Home from Process Picker
        btn_back_proc = [b for b in at.button if "Back to Home" in (b.label or "") or "वापस" in (b.label or "")][0]
        btn_back_proc.click().run()
        self.assertEqual(at.session_state["page"], "home")
        print("[OK] Step 3: Back to Home from Process Picker passed")

        # Step 4: Home -> Banking Services
        btn_bank = [b for b in at.button if "Banking" in (b.label or "") or "बैंकिंग" in (b.label or "")][0]
        btn_bank.click().run()
        self.assertEqual(at.session_state["page"], "process_picker")
        self.assertEqual(at.session_state["guide_category"], "banking")
        print("[OK] Step 4: Home -> Banking Guides passed")

        # Step 5: Back to Home from Banking
        btn_back_bank = [b for b in at.button if "Back to Home" in (b.label or "") or "वापस" in (b.label or "")][0]
        btn_back_bank.click().run()
        self.assertEqual(at.session_state["page"], "home")
        print("[OK] Step 5: Back to Home from Banking passed")

        # Step 6: Home -> Insurance Services
        btn_ins = [b for b in at.button if "Insurance" in (b.label or "") or "बीमा" in (b.label or "")][0]
        btn_ins.click().run()
        self.assertEqual(at.session_state["page"], "process_picker")
        self.assertEqual(at.session_state["guide_category"], "insurance")
        print("[OK] Step 6: Home -> Insurance Guides passed")

        # Step 7: Process Picker -> Open in Action Dashboard
        btn_open_dash = [b for b in at.button if "Open in Action Dashboard" in (b.label or "") or "डैशबोर्ड में खोलें" in (b.label or "")][0]
        btn_open_dash.click().run()
        self.assertEqual(at.session_state["page"], "dashboard")
        self.assertIsNotNone(at.session_state["analysis_result"])
        print("[OK] Step 7: Process Picker -> Action Dashboard passed")

        # Step 8: Dashboard Checkbox Check & Persistence
        chk = at.checkbox[0]
        chk.check().run()
        self.assertTrue(at.session_state["step_progress"].get("task_step_0"))
        print("[OK] Step 8: Step checklist checkbox checked and persisted in session state")

        # Step 9: Back to Home from Dashboard
        btn_back_dash = [b for b in at.button if "Back to Home" in (b.label or "") or "वापस" in (b.label or "")][0]
        btn_back_dash.click().run()
        self.assertEqual(at.session_state["page"], "home")
        print("[OK] Step 9: Back to Home from Dashboard passed")

        # Step 10: Home -> Upload Flow
        btn_upload = [b for b in at.button if "Upload" in (b.label or "") or "अपलोड" in (b.label or "")][0]
        btn_upload.click().run()
        self.assertEqual(at.session_state["page"], "upload")
        print("[OK] Step 10: Home -> Upload page passed")

        # Step 11: Back to Home from Upload
        btn_back_up = [b for b in at.button if "Back to Home" in (b.label or "") or "वापस" in (b.label or "")][0]
        btn_back_up.click().run()
        self.assertEqual(at.session_state["page"], "home")
        print("[OK] Step 11: Back to Home from Upload page passed")

        # Step 12: Ask AI Page & Back to Home
        at.session_state["page"] = "ask"
        at.run()
        self.assertEqual(at.session_state["page"], "ask")
        btn_back_ask = [b for b in at.button if "Back to Home" in (b.label or "") or "वापस" in (b.label or "") or "home" in b.key.lower()][0]
        btn_back_ask.click().run()
        self.assertEqual(at.session_state["page"], "home")
        print("[OK] Step 12: Ask AI page -> Back to Home passed")

        # Step 13: Verify Start Over is removed and check Completed Tasks navigation
        start_over_btns = [b for b in at.button if "Start Over" in (b.label or "") or "प्रारंभ" in (b.label or "")]
        self.assertEqual(len(start_over_btns), 0)
        btn_comp = [b for b in at.button if "Completed Task" in (b.label or "") or "पूर्ण" in (b.label or "")][0]
        btn_comp.click().run()
        self.assertEqual(at.session_state["page"], "completed_task")
        print("[OK] Step 13: Completed Tasks categorized view reached cleanly with no Start Over button")

        # Step 14: Sidebar Sign Out
        btn_signout = [b for b in at.button if "Sign Out" in (b.label or "") or "साइन आउट" in (b.label or "")][0]
        btn_signout.click().run()
        self.assertEqual(at.session_state["page"], "login")
        self.assertIsNone(at.session_state["user"])
        print("[OK] Step 14: Sign Out cleared session state cleanly back to Login")

if __name__ == "__main__":
    unittest.main()
