import os
import zipfile
from datetime import datetime

root_dir = os.path.dirname(os.path.abspath(__file__))
output_md = os.path.join(root_dir, "ALL_PROJECT_CODE.md")
output_zip = os.path.join(root_dir, "project_codebase_bundle.zip")

files_to_include = [
    "requirements.txt",
    "app.py",
    "data/processes.json",
    "logic/__init__.py",
    "logic/extract_text.py",
    "logic/llm_calls.py",
    "logic/process_data.py",
    "logic/grok_calls.py",
    "pages/login.py",
    "pages/home.py",
    "pages/upload.py",
    "pages/process_picker.py",
    "pages/dashboard.py",
    "pages/ask.py",
    "test_comprehensive.py"
]

# 1. Create Consolidated Markdown File
with open(output_md, "w", encoding="utf-8") as out:
    out.write("# 🇮🇳 Multilingual Document & Indian Government Process Assistant\n\n")
    out.write(f"**Consolidated Project Codebase**\n")
    out.write(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
    out.write("---\n\n")
    out.write("## 📁 Project Architecture & Table of Contents\n\n")
    
    for fpath in files_to_include:
        out.write(f"- [`{fpath}`](#{fpath.replace('/', '-').replace('.', '-')})\n")
    out.write("\n---\n\n")
    
    for fpath in files_to_include:
        full_path = os.path.join(root_dir, fpath)
        if os.path.exists(full_path):
            out.write(f"## 📄 `{fpath}`\n\n")
            ext = os.path.splitext(fpath)[1].replace(".", "")
            lang = "json" if ext == "json" else "python" if ext == "py" else "text"
            out.write(f"```{lang}\n")
            with open(full_path, "r", encoding="utf-8", errors="replace") as sf:
                out.write(sf.read())
            out.write("\n```\n\n---\n\n")

# 2. Create Zip Archive Bundle
with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for fpath in files_to_include:
        full_path = os.path.join(root_dir, fpath)
        if os.path.exists(full_path):
            zipf.write(full_path, arcname=fpath)

print("Created:", output_md, f"({os.path.getsize(output_md)} bytes)")
print("Created:", output_zip, f"({os.path.getsize(output_zip)} bytes)")
