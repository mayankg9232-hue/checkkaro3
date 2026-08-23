import unittest
import os
from dotenv import load_dotenv

class TestEnvAndGitignore(unittest.TestCase):

    def test_01_env_file_exists_and_configured(self):
        print("\n--- 1. Testing .env File Configuration ---")
        self.assertTrue(os.path.exists(".env"), ".env file must exist in project root")
        
        with open(".env", "r", encoding="utf-8") as f:
            content = f.read()
            
        self.assertTrue(any("GROQ_API_KEY" in line for line in content.splitlines()), ".env must contain GROQ_API_KEY")
        print("[OK] .env file contains GROQ_API_KEY")

    def test_02_gitignore_file_configured(self):
        print("\n--- 2. Testing .gitignore File Configuration ---")
        self.assertTrue(os.path.exists(".gitignore"), ".gitignore file must exist in project root")
        
        with open(".gitignore", "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
            
        ignored_items = [l.strip() for l in lines if l.strip() and not l.startswith("#")]
        self.assertIn(".env", ignored_items)
        self.assertIn("__pycache__/", ignored_items)
        print("[OK] .gitignore properly ignores .env and Python cache/venv files")

    def test_03_llm_calls_reads_env_key(self):
        print("\n--- 3. Testing logic/llm_calls API key binding ---")
        load_dotenv(override=True)
        import logic.llm_calls as lc
        
        self.assertTrue(bool(lc.GROQ_API_KEY), "GROQ_API_KEY in logic.llm_calls should be loaded and non-empty")
        print("[OK] logic/llm_calls successfully reads the key from environment")

if __name__ == "__main__":
    unittest.main()
