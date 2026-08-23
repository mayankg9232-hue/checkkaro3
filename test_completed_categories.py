import unittest
from streamlit.testing.v1 import AppTest

class TestCompletedCategoriesAndNoStartOver(unittest.TestCase):

    def test_01_no_start_over_button_exists(self):
        print("\n--- 1. Testing Start Over Button Removal ---")
        at = AppTest.from_file("app.py", default_timeout=20)
        at.run()

        # Login
        at.text_input[0].input("Rohan Joshi")
        at.button[0].click().run()
        self.assertEqual(at.session_state["page"], "home")

        # Verify no Start Over button exists in sidebar or anywhere on Home
        start_over_btns = [b for b in at.button if "Start Over" in (b.label or "") or "पुनः प्रारंभ" in (b.label or "")]
        self.assertEqual(len(start_over_btns), 0, "Start Over button should be removed entirely")
        print("[OK] Start Over button is completely removed from sidebar and application")

    def test_02_completed_tasks_by_category(self):
        print("\n--- 2. Testing Completed Tasks Categorization (Expander Grouping) ---")
        at = AppTest.from_file("app.py", default_timeout=20)
        at.run()

        # Login
        at.text_input[0].input("Rohan Joshi")
        at.button[0].click().run()

        # 1. Government Guide
        btn_govt = [b for b in at.button if "Government" in (b.label or "") or "सरकारी" in (b.label or "")][0]
        btn_govt.click().run()
        self.assertEqual(at.session_state["guide_category"], "government")

        # 2. Banking Guide
        [b for b in at.button if "Back to Home" in (b.label or "") or "वापस" in (b.label or "")][0].click().run()
        btn_bank = [b for b in at.button if "Banking" in (b.label or "") or "बैंकिंग" in (b.label or "")][0]
        btn_bank.click().run()
        self.assertEqual(at.session_state["guide_category"], "banking")

        # 3. Insurance Guide
        [b for b in at.button if "Back to Home" in (b.label or "") or "वापस" in (b.label or "")][0].click().run()
        btn_ins = [b for b in at.button if "Insurance" in (b.label or "") or "बीमा" in (b.label or "")][0]
        btn_ins.click().run()
        self.assertEqual(at.session_state["guide_category"], "insurance")

        # 4. Navigate to Completed Task section via Sidebar
        btn_comp = [b for b in at.button if "Completed Task" in (b.label or "") or "पूर्ण कार्य" in (b.label or "")][0]
        btn_comp.click().run()
        self.assertEqual(at.session_state["page"], "completed_task")

        # Verify expanders exist for categories
        expanders = at.expander
        self.assertTrue(len(expanders) >= 4, "Should render 4 category expanders")
        
        # Verify expander labels contain category names and counts
        exp_labels = [e.label for e in expanders]
        self.assertTrue(any("Document" in l or "दस्तावेज़" in l for l in exp_labels))
        self.assertTrue(any("Government" in l or "सरकारी" in l for l in exp_labels))
        self.assertTrue(any("Banking" in l or "बैंकिंग" in l for l in exp_labels))
        self.assertTrue(any("Insurance" in l or "बीमा" in l for l in exp_labels))

        print("[OK] Completed tasks cleanly organized by category with collapsible expanders")

    def test_03_sign_out_resets_session_cleanly(self):
        print("\n--- 3. Testing Sign Out Behavior ---")
        at = AppTest.from_file("app.py", default_timeout=20)
        at.run()

        # Login
        at.text_input[0].input("Rohan Joshi")
        at.button[0].click().run()
        self.assertEqual(at.session_state["page"], "home")

        # Sign Out
        btn_sign = [b for b in at.button if "Sign Out" in (b.label or "") or "साइन आउट" in (b.label or "")][0]
        btn_sign.click().run()
        self.assertEqual(at.session_state["page"], "login")
        self.assertIsNone(at.session_state["user"])
        print("[OK] Sign Out cleanly cleared session state back to login")

if __name__ == "__main__":
    unittest.main()
