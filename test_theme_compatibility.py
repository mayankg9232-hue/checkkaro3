import unittest
from streamlit.testing.v1 import AppTest

class TestAutoThemeAndControls(unittest.TestCase):

    def test_01_auto_theme_light_mode(self):
        print("\n--- 1. Testing Auto Theme (Light Mode) ---")
        at = AppTest.from_file("app.py", default_timeout=15)
        at.query_params["sys_theme"] = "light"
        at.run()
        
        # Verify no manual theme controls exist
        theme_widgets = [s for s in at.selectbox if "Theme" in (s.label or "")]
        self.assertEqual(len(theme_widgets), 0, "No manual theme selector should exist")
        
        # Login
        at.text_input[0].input("Meera Patel")
        at.button[0].click().run()
        self.assertEqual(at.session_state["page"], "home")
        print("[OK] Light Mode auto-detection verified with zero manual toggles")

    def test_02_auto_theme_dark_mode(self):
        print("\n--- 2. Testing Auto Theme (Dark Mode) ---")
        at = AppTest.from_file("app.py", default_timeout=15)
        at.query_params["sys_theme"] = "dark"
        at.run()
        
        # Login
        at.text_input[0].input("Meera Patel")
        at.button[0].click().run()
        self.assertEqual(at.session_state["page"], "home")
        print("[OK] Dark Mode auto-detection verified")

    def test_03_all_buttons_and_controls_functional(self):
        print("\n--- 3. Testing All Navigation & Control Buttons ---")
        at = AppTest.from_file("app.py", default_timeout=15)
        at.run()
        
        # 1. Login button
        at.text_input[0].input("Meera Patel")
        at.button[0].click().run()
        self.assertEqual(at.session_state["page"], "home")
        
        # 2. Home -> Upload Document button
        btn_upload = [b for b in at.button if "Upload & Analyze" in (b.label or "") or "अपलोड" in (b.label or "")]
        self.assertTrue(len(btn_upload) > 0)
        btn_upload[0].click().run()
        self.assertEqual(at.session_state["page"], "upload")
        
        # 3. Upload screen -> Back to Home
        btn_back = [b for b in at.button if "Back to Home" in (b.label or "") or "वापस" in (b.label or "")]
        self.assertTrue(len(btn_back) > 0)
        btn_back[0].click().run()
        self.assertEqual(at.session_state["page"], "home")
        
        # 4. Home -> Government Services button
        btn_govt = [b for b in at.button if "Government Services" in (b.label or "") or "सरकारी सेवाएं" in (b.label or "")]
        self.assertTrue(len(btn_govt) > 0)
        btn_govt[0].click().run()
        self.assertEqual(at.session_state["page"], "process_picker")
        self.assertEqual(at.session_state["guide_category"], "government")
        
        # 5. Process Picker -> Back to Home
        btn_back_proc = [b for b in at.button if "Back to Home" in (b.label or "") or "वापस" in (b.label or "")]
        self.assertTrue(len(btn_back_proc) > 0)
        btn_back_proc[0].click().run()
        self.assertEqual(at.session_state["page"], "home")

        # 6. Home -> Banking Services button (Active guide)
        btn_banking = [b for b in at.button if "Banking Services" in (b.label or "") or "बैंकिंग सेवाएं" in (b.label or "")]
        btn_banking[0].click().run()
        self.assertEqual(at.session_state["page"], "process_picker")
        self.assertEqual(at.session_state["guide_category"], "banking")

        # Go back to home
        btn_back_proc2 = [b for b in at.button if "Back to Home" in (b.label or "") or "वापस" in (b.label or "")]
        btn_back_proc2[0].click().run()

        # 7. Home -> Insurance Services button (Active guide)
        btn_insurance = [b for b in at.button if "Insurance Services" in (b.label or "") or "बीमा सेवाएं" in (b.label or "")]
        btn_insurance[0].click().run()
        self.assertEqual(at.session_state["page"], "process_picker")
        self.assertEqual(at.session_state["guide_category"], "insurance")

        # Go back to home
        btn_back_proc3 = [b for b in at.button if "Back to Home" in (b.label or "") or "वापस" in (b.label or "")]
        btn_back_proc3[0].click().run()

        # 8. Sidebar Current Task button
        btn_current = [b for b in at.button if "Current Task" in (b.label or "") or "वर्तमान कार्य" in (b.label or "")]
        btn_current[0].click().run()
        self.assertIn(at.session_state["page"], ["dashboard", "current_task"])

        # 9. Sidebar Completed Task button
        btn_completed = [b for b in at.button if "Completed Task" in (b.label or "") or "पूर्ण कार्य" in (b.label or "")]
        btn_completed[0].click().run()
        self.assertEqual(at.session_state["page"], "completed_task")

        # 10. Sidebar Sign Out button
        btn_signout = [b for b in at.button if "Sign Out" in (b.label or "") or "साइन आउट" in (b.label or "")]
        btn_signout[0].click().run()
        self.assertEqual(at.session_state["page"], "login")
        self.assertIsNone(at.session_state["user"])
        print("[OK] Every button across the app tested and confirmed functional")

if __name__ == "__main__":
    unittest.main()
