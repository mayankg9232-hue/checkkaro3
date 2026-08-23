import unittest
from streamlit.testing.v1 import AppTest
from logic.translations import t, get_normalized_language, TRANSLATIONS
from logic.process_data import load_processes, get_process_by_id

class TestMultilingualSupport(unittest.TestCase):

    def test_01_translation_function(self):
        print("\n--- 1. Testing Translation System (English, Hindi, Kannada) ---")
        self.assertEqual(get_normalized_language("Hindi (हिंदी)"), "Hindi")
        self.assertEqual(get_normalized_language("Kannada (ಕನ್ನಡ)"), "Kannada")
        self.assertEqual(get_normalized_language("English"), "English")

        # Test English strings
        self.assertEqual(t("home", "English"), "🏠 Home")
        self.assertEqual(t("sign_out", "English"), "🚪 Sign Out")

        # Test Hindi strings
        self.assertEqual(t("home", "Hindi"), "🏠 होम")
        self.assertEqual(t("sign_out", "Hindi"), "🚪 साइन आउट")
        self.assertIn("नमस्ते", t("welcome_greeting", "Hindi", user_name="रोहन"))

        # Test Kannada strings
        self.assertEqual(t("home", "Kannada"), "🏠 ಮುಖಪುಟ")
        self.assertEqual(t("sign_out", "Kannada"), "🚪 ಸೈನ್ ಔಟ್")
        self.assertIn("ಸ್ವಾಗತ", t("welcome_greeting", "Kannada", user_name="ರೋಹನ್"))

        # Fallback test
        self.assertEqual(t("non_existent_key_xyz", "Hindi"), "non_existent_key_xyz")
        print("[OK] Central translation system verified across all 3 languages")

    def test_02_localized_processes(self):
        print("\n--- 2. Testing Curated Process Data Localization ---")
        procs_en = load_processes("English")
        self.assertEqual(procs_en[0]["name"], "New PAN Card Application (Form 49A)")

        procs_hi = load_processes("Hindi")
        self.assertIn("पैन कार्ड", procs_hi[0]["name"])
        self.assertIn("आयकर", procs_hi[0]["description"])
        self.assertIn("आधार कार्ड", procs_hi[0]["required_documents"][0])

        procs_kn = load_processes("Kannada")
        self.assertIn("ಪ್ಯಾನ್", procs_kn[0]["name"])
        self.assertIn("ಆದಾಯ ತೆರಿಗೆ", procs_kn[0]["description"])
        print("[OK] Curated Government Process Guides localized accurately")

    def test_03_app_ui_hindi_end_to_end(self):
        print("\n--- 3. Testing End-to-End App Navigation in Hindi ---")
        at = AppTest.from_file("app.py", default_timeout=15)
        at.session_state["language"] = "Hindi"
        at.run()

        # Login in Hindi
        at.text_input[0].input("राजेश कुमार")
        at.button[0].click().run()

        self.assertEqual(at.session_state["page"], "home")
        self.assertEqual(at.session_state["language"], "Hindi")

        # Verify Home screen buttons in Hindi
        btn_labels = [b.label for b in at.button if b.label]
        self.assertTrue(any("सरकारी सेवाएं" in lbl for lbl in btn_labels))
        print("[OK] Home screen fully rendered in Hindi")

    def test_04_app_ui_kannada_end_to_end(self):
        print("\n--- 4. Testing End-to-End App Navigation in Kannada ---")
        at = AppTest.from_file("app.py", default_timeout=15)
        at.session_state["language"] = "Kannada"
        at.run()

        # Login in Kannada
        at.text_input[0].input("ಸುರೇಶ್ ಕುಮಾರ್")
        at.button[0].click().run()

        self.assertEqual(at.session_state["page"], "home")
        self.assertEqual(at.session_state["language"], "Kannada")

        # Verify Home screen buttons in Kannada
        btn_labels = [b.label for b in at.button if b.label]
        self.assertTrue(any("ಸರ್ಕಾರಿ ಸೇವೆಗಳನ್ನು" in lbl for lbl in btn_labels))
        print("[OK] Home screen fully rendered in Kannada")

if __name__ == "__main__":
    unittest.main()
