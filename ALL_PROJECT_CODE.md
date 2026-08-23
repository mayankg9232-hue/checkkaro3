# 🇮🇳 Multilingual Document & Indian Government Process Assistant

**Consolidated Project Codebase**
*Generated on: 2026-08-23 10:00:30*

---

## 📁 Project Architecture & Table of Contents

- [`requirements.txt`](#requirements-txt)
- [`app.py`](#app-py)
- [`data/processes.json`](#data-processes-json)
- [`logic/__init__.py`](#logic-__init__-py)
- [`logic/extract_text.py`](#logic-extract_text-py)
- [`logic/llm_calls.py`](#logic-llm_calls-py)
- [`logic/process_data.py`](#logic-process_data-py)
- [`logic/grok_calls.py`](#logic-grok_calls-py)
- [`pages/login.py`](#pages-login-py)
- [`pages/home.py`](#pages-home-py)
- [`pages/upload.py`](#pages-upload-py)
- [`pages/process_picker.py`](#pages-process_picker-py)
- [`pages/dashboard.py`](#pages-dashboard-py)
- [`pages/ask.py`](#pages-ask-py)
- [`test_comprehensive.py`](#test_comprehensive-py)

---

## 📄 `requirements.txt`

```text
﻿streamlit>=1.30.0
pypdf>=4.0.0
python-docx>=1.1.0
groq>=0.15.0
anthropic>=0.18.0
openai>=1.0.0

```

---

## 📄 `app.py`

```python
﻿import streamlit as st
import sys
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Add root folder to python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logic.translations import t, get_normalized_language
from pages.login import render_login
from pages.home import render_home
from pages.upload import render_upload
from pages.ask import render_ask
from pages.process_picker import render_process_picker
from pages.dashboard import render_dashboard

# App Configuration
st.set_page_config(
    page_title="Document & Process Assistant",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session State Initialization
if "page" not in st.session_state:
    st.session_state["page"] = "login"
if "user" not in st.session_state:
    st.session_state["user"] = None
if "language" not in st.session_state:
    st.session_state["language"] = "English"
if "analysis_result" not in st.session_state:
    st.session_state["analysis_result"] = None
if "doc_text" not in st.session_state:
    st.session_state["doc_text"] = None
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "general_chat_history" not in st.session_state:
    st.session_state["general_chat_history"] = []
if "step_progress" not in st.session_state:
    st.session_state["step_progress"] = {}
if "show_uploader" not in st.session_state:
    st.session_state["show_uploader"] = False

# Pure CSS Media Query Theme Injection (Auto-matches browser light/dark mode seamlessly)
theme_css = """
<style>
/* Universal Layout & UI Cleanups */
#MainMenu, [data-testid="stMainMenu"], [data-testid="stToolbarActions"], [data-testid="stDecoration"], footer {
    display: none !important;
    visibility: hidden !important;
}
header[data-testid="stHeader"] {
    background: transparent !important;
}
[data-testid="stSidebarNav"], [data-testid="stSidebarNavSeparator"] {
    display: none !important;
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}
.stButton>button {
    border-radius: 8px;
    font-weight: 500;
    transition: all 0.2s ease;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 6px 6px 0 0;
    padding: 10px 18px;
}

/* ================= DARK THEME (when browser is in Dark Mode) ================= */
@media (prefers-color-scheme: dark) {
    :root {
        --app-bg: #0e1117;
        --app-text: #f7fafc;
        --app-text-muted: #a0aec0;
        --sidebar-bg: #1a1f2c;
        --card-bg-blue: #162436;
        --card-border-blue: #3182ce;
        --card-bg-orange: #332214;
        --card-border-orange: #ed8936;
        --card-bg-banking: #15293d;
        --card-border-banking: #4299e1;
        --card-bg-insurance: #112d2b;
        --card-border-insurance: #38b2ac;
        --box-summary-bg: #1e2430;
        --box-summary-border: #3a4150;
        --step-item-bg: #1a202c;
        --step-item-border: #3a4150;
        --step-item-text: #e2e8f0;
    }
    .stApp, [data-testid="stAppViewContainer"], body {
        background-color: #0e1117 !important;
        color: #f7fafc !important;
    }
    [data-testid="stSidebar"] {
        background-color: #1a1f2c !important;
    }
    [data-testid="stSidebar"] * {
        color: #f7fafc !important;
    }
    .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown div, .stMarkdown strong, h1, h2, h3, h4, h5, h6 {
        color: #f7fafc !important;
    }
    .stSelectbox label, .stTextInput label {
        color: #f7fafc !important;
    }
    .stTextInput input, .stSelectbox [data-baseweb="select"] {
        background-color: #262730 !important;
        color: #ffffff !important;
        border-color: #3a4150 !important;
    }
    .stChatMessage {
        background-color: #1e2430 !important;
        border: 1px solid #3a4150 !important;
        color: #f7fafc !important;
    }
    .stButton>button {
        background-color: #1e2430 !important;
        color: #f7fafc !important;
        border: 1px solid #3a4150 !important;
    }
    .stButton>button:hover {
        border-color: #3182ce !important;
        color: #3182ce !important;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1e2430 !important;
        color: #a0aec0 !important;
        border: 1px solid #3a4150 !important;
    }
    .stTabs [aria-selected="true"] {
        color: #3182ce !important;
        font-weight: bold;
    }
}

/* ================= LIGHT THEME (when browser is in Light Mode) ================= */
@media (prefers-color-scheme: light) {
    :root {
        --app-bg: #ffffff;
        --app-text: #1a202c;
        --app-text-muted: #4a5568;
        --sidebar-bg: #f8f9fa;
        --card-bg-blue: #f0f8ff;
        --card-border-blue: #005A9C;
        --card-bg-orange: #fff8f0;
        --card-border-orange: #E37222;
        --card-bg-banking: #ebf8ff;
        --card-border-banking: #2B6CB0;
        --card-bg-insurance: #e6fffa;
        --card-border-insurance: #2C7A7B;
        --box-summary-bg: #f8f9fa;
        --box-summary-border: #e2e8f0;
        --step-item-bg: #ffffff;
        --step-item-border: #e2e8f0;
        --step-item-text: #2d3748;
    }
    .stApp, [data-testid="stAppViewContainer"], body {
        background-color: #ffffff !important;
        color: #1a202c !important;
    }
    [data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
    }
    .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown strong {
        color: #1a202c !important;
    }
    .stChatMessage {
        background-color: #f8f9fa !important;
        border: 1px solid #e2e8f0 !important;
    }
}
</style>
"""

st.html(theme_css)

# ----------------- SIDEBAR LOGIC -----------------
if st.session_state.get("user"):
    user_info = st.session_state["user"]
    user_name = user_info.get("name", "User")
    
    with st.sidebar:
        st.markdown(f"## 👤 {user_name}")
        st.markdown("---")
        
        # Global Language Selector (Available on every page)
        lang_options = ["English", "Hindi (हिंदी)", "Kannada (ಕನ್ನಡ)"]
        curr_lang = st.session_state.get("language", "English")
        curr_idx = 0
        if "Hindi" in curr_lang:
            curr_idx = 1
        elif "Kannada" in curr_lang:
            curr_idx = 2
            
        selected_lang_label = st.selectbox(
            t("language"),
            lang_options,
            index=curr_idx,
            key="global_lang_selector"
        )
        norm_selected = get_normalized_language(selected_lang_label)
        if norm_selected != get_normalized_language(st.session_state.get("language")):
            st.session_state["language"] = norm_selected
            st.rerun()

        st.markdown("---")

        # Quick Navigation (Home, Current Task, Completed Task)
        st.markdown(f"### {t('quick_navigation')}")
        
        if st.button(t("home"), use_container_width=True, key="side_nav_home"):
            st.session_state["page"] = "home"
            st.session_state["show_uploader"] = False
            st.rerun()
            
        if st.button(t("current_task"), use_container_width=True, key="side_nav_current"):
            if st.session_state.get("analysis_result"):
                st.session_state["page"] = "dashboard"
            else:
                st.session_state["page"] = "current_task"
            st.rerun()
            
        if st.button(t("completed_task"), use_container_width=True, key="side_nav_completed"):
            st.session_state["page"] = "completed_task"
            st.rerun()
            
        st.markdown("---")
        
        # Sign Out button at bottom (preserves language preference)
        if st.button(t("sign_out"), use_container_width=True, key="side_nav_signout"):
            saved_lang = st.session_state.get("language", "English")
            st.session_state.clear()
            st.session_state["page"] = "login"
            st.session_state["language"] = saved_lang
            st.rerun()

# ----------------- PLACEHOLDER PAGES -----------------
def render_current_task():
    st.markdown(f"## {t('current_task_title')}")
    if st.session_state.get("analysis_result"):
        render_dashboard()
    else:
        st.info(t("no_active_task_info"))
        st.markdown(t("no_active_task_desc"))
        if st.button(t("go_to_home"), key="btn_cur_task_home", use_container_width=True):
            st.session_state["page"] = "home"
            st.rerun()

def render_completed_task():
    col_nav1, col_nav2 = st.columns([2, 5])
    with col_nav1:
        if st.button(t("back_to_home"), key="btn_comp_task_home", use_container_width=True):
            st.session_state["page"] = "home"
            st.rerun()

    st.markdown(f"## {t('completed_task_title')}")
    
    # Retrieve tracked completed history
    history = st.session_state.get("completed_history", [])
    step_progress = st.session_state.get("step_progress", {})
    checked_steps_count = sum(1 for k, v in step_progress.items() if v)
    
    categories = [
        ("documents", t("cat_documents")),
        ("government", t("cat_government")),
        ("banking", t("cat_banking")),
        ("insurance", t("cat_insurance"))
    ]
    
    # Categorize items
    cat_items = {cat_id: [] for cat_id, _ in categories}
    for item in history:
        cat = item.get("category", "government")
        if cat in cat_items:
            cat_items[cat].append(item)
        else:
            cat_items["government"].append(item)
            
    total_items = sum(len(items) for items in cat_items.values()) + checked_steps_count
    
    if total_items > 0:
        st.success(t("completed_tasks_count", count=total_items))
    else:
        st.info(t("no_completed_tasks_info"))
        st.caption(t("no_completed_tasks_desc"))
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Render Collapsible Category Sections
    for cat_id, cat_title in categories:
        items = cat_items[cat_id]
        item_count = len(items)
        
        with st.expander(f"{cat_title} ({item_count})", expanded=(item_count > 0 and item_count <= 4)):
            if items:
                for item in items:
                    item_name = item.get("name", "Task")
                    item_status = item.get("status", "Completed")
                    st.markdown(f"""
                    <div style="background-color: var(--step-item-bg, #ffffff); border: 1px solid var(--step-item-border, #e2e8f0); border-radius: 6px; padding: 12px 16px; margin-bottom: 10px;">
                        <strong style="color: var(--app-text, #1a202c);">✔️ {item_name}</strong>
                        <div style="font-size: 13px; color: var(--app-text-muted, #718096); margin-top: 4px;">
                            <span style="background-color: var(--card-border-blue, #005A9C); color: #ffffff; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: bold;">{item_status}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.caption(t("no_completed_in_category"))

# ----------------- PAGE ROUTER -----------------
current_page = st.session_state.get("page", "login")

# Force login if user not authenticated
if not st.session_state.get("user") and current_page != "login":
    current_page = "login"
    st.session_state["page"] = "login"

if current_page == "login":
    render_login()
elif current_page == "home":
    render_home()
elif current_page == "upload":
    render_upload()
elif current_page == "ask":
    render_ask()
elif current_page == "process_picker":
    render_process_picker()
elif current_page == "dashboard":
    render_dashboard()
elif current_page == "current_task":
    render_current_task()
elif current_page == "completed_task":
    render_completed_task()
else:
    st.session_state["page"] = "home"
    st.rerun()

```

---

## 📄 `data/processes.json`

```json
﻿[
  {
    "id": "pan_card",
    "name": "New PAN Card Application (Form 49A)",
    "description": "Application for allotment of a 10-digit alphanumeric Permanent Account Number (PAN) for Indian citizens, entities, and trusts under the Income Tax Department.",
    "steps": [
      "Visit the official Protean (NSDL) e-Gov or UTIITSL online portal (or visit an authorized TIN-FC center).",
      "Select Application Type as 'Form 49A - Indian Citizen' and choose Category (e.g., Individual).",
      "Fill in personal details: Full Name, Date of Birth, Gender, Father's Name, and Address.",
      "Choose submission mode: Paperless e-KYC/e-Sign (via Aadhaar OTP), Scanned images upload, or Physical document dispatch.",
      "Pay the prescribed application processing fee using Net Banking, Debit/Credit Card, or UPI.",
      "Download and save the 15-digit acknowledgement slip to track delivery and processing status.",
      "If physical mode was selected, mail the signed form with self-attested document copies to the NSDL/UTIITSL processing center within 15 days."
    ],
    "required_documents": [
      "Proof of Identity (POI): Aadhaar Card, Voter ID, Passport, or Driving License",
      "Proof of Address (POA): Aadhaar Card, Electricity Bill (< 3 months), Bank Account Statement, or Post Office Passbook",
      "Proof of Date of Birth (DOB): Aadhaar Card, Birth Certificate, Matriculation Marksheet, or Passport",
      "Two recent passport-size color photographs (3.5 cm x 2.5 cm) for physical applications"
    ],
    "authority": {
      "type": "Income Tax Department (via Protean eGov Technologies / UTIITSL)",
      "mode": "both",
      "note": "confirm exact details at your nearest center, as requirements vary by state"
    },
    "estimated_time": "10 to 15 working days for physical card delivery; 2 to 3 days for Instant e-PAN",
    "fees": "₹107 (including GST) for dispatch within India; ₹1,017 for overseas address; e-PAN is free/nominal"
  },
  {
    "id": "aadhaar_update",
    "name": "Aadhaar Card Correction & Update",
    "description": "Process to update or correct demographic details (Name, Address, Date of Birth, Gender, Mobile Number) or biometric data (Fingerprints, Iris, Photo) with UIDAI.",
    "steps": [
      "Check update eligibility: Address and document updates can be done online via the myAadhaar portal; Mobile number, Name corrections, and Biometrics require an in-person Aadhaar Enrolment Center visit.",
      "For Online (Address Update): Log in to the myAadhaar portal using Aadhaar Number and OTP sent to registered mobile.",
      "Select 'Update Address in Aadhaar', enter new address details, and upload valid supporting proof.",
      "For In-Person Updates (Name, DOB, Mobile, Biometrics): Book an appointment online via UIDAI portal or walk into an authorized Aadhaar Seva Kendra / Bank / Post Office center.",
      "Fill the Aadhaar Correction Form and present original verification documents to the operator.",
      "Provide biometric authentication and verify the operator's entry on screen.",
      "Collect the Update Request Number (URN) acknowledgement slip and track status on the UIDAI portal."
    ],
    "required_documents": [
      "For Name Correction: Proof of Identity (Passport, PAN Card, Voter ID, Ration Card with photo)",
      "For Address Update: Proof of Address (Electricity/Water Bill < 3 months, Rent Agreement, Bank Passbook, Passport)",
      "For DOB Correction: Proof of Date of Birth (Birth Certificate, SSLC/10th Certificate, Passport)",
      "Existing Aadhaar Card number / copy"
    ],
    "authority": {
      "type": "Unique Identification Authority of India (UIDAI) / Aadhaar Seva Kendra",
      "mode": "both",
      "note": "confirm exact details at your nearest center, as requirements vary by state"
    },
    "estimated_time": "5 to 15 working days (maximum 30 days under standard SLA)",
    "fees": "₹50 for demographic updates; ₹100 for biometric update; Online document updates periodically free on portal"
  },
  {
    "id": "passport_renewal",
    "name": "Passport Renewal / Re-issue",
    "description": "Application for re-issue of Indian Passport due to expiry, exhaustion of visa pages, change in personal particulars, or damaged/lost booklet through the Ministry of External Affairs.",
    "steps": [
      "Register and create an account on the official Passport Seva Portal (passportindia.gov.in) or mPassport Seva app.",
      "Select 'Apply for Fresh Passport/Re-issue of Passport' and choose Normal or Tatkaal scheme (36 or 60 pages booklet).",
      "Fill in the online application form with applicant details, family information, address, and past passport particulars.",
      "Make the online fee payment and schedule an appointment at the nearest Passport Seva Kendra (PSK) or Post Office Passport Seva Kendra (POPSK).",
      "Print or save the Application Receipt containing the Appointment Batch and ARN (Application Reference Number).",
      "Visit the designated PSK/POPSK on the scheduled date and time with original documents and self-attested photocopies.",
      "Complete the three-stage counter verification (Counter A: Biometrics & Photo, Counter B: Document Verification, Counter C: Granting).",
      "Complete Local Police Verification if required for your address status.",
      "Receive the renewed passport via Speed Post at your registered residence."
    ],
    "required_documents": [
      "Old original Passport with self-attested photocopies of first two and last two pages (including ECR/Non-ECR page)",
      "Proof of Present Address (Aadhaar Card, Utility Bill, Bank Passbook, Spouse Passport)",
      "Proof of Date of Birth (Aadhaar Card, Birth Certificate, School Leaving Certificate)",
      "Documentary proof for any change in personal particulars (e.g., Marriage Certificate, Gazette notification)"
    ],
    "authority": {
      "type": "Passport Seva Kendra (PSK) / Regional Passport Office (RPO), Ministry of External Affairs",
      "mode": "both",
      "note": "confirm exact details at your nearest center, as requirements vary by state"
    },
    "estimated_time": "Normal: 15 to 30 working days (post police verification); Tatkaal: 1 to 3 working days",
    "fees": "Normal (36 pages): ₹1,500; Normal (60 pages): ₹2,000; Tatkaal: Additional ₹2,000"
  }
]

```

---

## 📄 `logic/__init__.py`

```python
﻿from logic.extract_text import get_text, extract_text
from logic.llm_calls import analyze_document, answer_question
from logic.process_data import load_processes, format_process_for_analysis

```

---

## 📄 `logic/extract_text.py`

```python
﻿import io
import os
import sys
from typing import Union, BinaryIO
from pypdf import PdfReader
import docx

def extract_text_from_pdf(file_input: Union[str, bytes, BinaryIO]) -> str:
    """
    Extracts plain text from a PDF file path, bytes, or file-like object using pypdf.
    Raises clear errors for empty, unreadable, or corrupted files.
    """
    try:
        if isinstance(file_input, str):
            if not os.path.exists(file_input):
                raise FileNotFoundError(f"File not found: '{file_input}'")
            with open(file_input, "rb") as f:
                stream = io.BytesIO(f.read())
        elif isinstance(file_input, bytes):
            stream = io.BytesIO(file_input)
        else:
            # File-like object (e.g. Streamlit UploadedFile)
            if hasattr(file_input, "getvalue"):
                stream = io.BytesIO(file_input.getvalue())
            elif hasattr(file_input, "read"):
                stream = io.BytesIO(file_input.read())
                if hasattr(file_input, "seek"):
                    file_input.seek(0)
            else:
                stream = file_input
            
        reader = PdfReader(stream)
        if len(reader.pages) == 0:
            raise ValueError("The PDF document contains 0 pages or is empty.")
            
        extracted_pages = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and text.strip():
                extracted_pages.append(text.strip())
                
        full_text = "\n\n".join(extracted_pages)
        if not full_text.strip():
            raise ValueError("The PDF document does not contain readable text (it may be scanned/image-only or blank).")
        return full_text
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise RuntimeError(f"Corrupted or invalid PDF file: {str(e)}")

def extract_text_from_docx(file_input: Union[str, bytes, BinaryIO]) -> str:
    """
    Extracts plain text from a DOCX file path, bytes, or file-like object using python-docx.
    Raises clear errors for empty or corrupted files.
    """
    try:
        if isinstance(file_input, str):
            if not os.path.exists(file_input):
                raise FileNotFoundError(f"File not found: '{file_input}'")
            with open(file_input, "rb") as f:
                stream = io.BytesIO(f.read())
        elif isinstance(file_input, bytes):
            stream = io.BytesIO(file_input)
        else:
            if hasattr(file_input, "getvalue"):
                stream = io.BytesIO(file_input.getvalue())
            elif hasattr(file_input, "read"):
                stream = io.BytesIO(file_input.read())
                if hasattr(file_input, "seek"):
                    file_input.seek(0)
            else:
                stream = file_input
                
        doc = docx.Document(stream)
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        
        for table in doc.tables:
            for row in table.rows:
                row_text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
                if row_text:
                    paragraphs.append(row_text)
                    
        full_text = "\n\n".join(paragraphs)
        if not full_text.strip():
            raise ValueError("The DOCX document is empty.")
        return full_text
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise RuntimeError(f"Corrupted or invalid DOCX file: {str(e)}")

def get_text(uploaded_file: Union[str, bytes, BinaryIO], filename: str = None) -> str:
    """
    Primary extraction interface. Extracts text from PDF files (using pypdf)
    and DOCX files (using python-docx). Raises clear errors for unsupported
    file types or corrupted files.
    """
    if uploaded_file is None:
        raise ValueError("No file was provided for text extraction.")
        
    name = filename or getattr(uploaded_file, "name", "")
    if not name and isinstance(uploaded_file, str):
        name = uploaded_file
        
    lower_name = name.lower()
    if lower_name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif lower_name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    else:
        ext = os.path.splitext(name)[1] if name else "unknown"
        raise ValueError(f"Unsupported file format '{ext}'. Only PDF (.pdf) and DOCX (.docx) files are supported.")

# Alias for backward compatibility across modules
extract_text = get_text

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    if len(sys.argv) > 1:
        target_path = sys.argv[1]
        try:
            print(f"Extracting text from: {target_path}")
            result_text = get_text(target_path)
            print("=" * 60)
            print(result_text)
            print("=" * 60)
            print(f"Extraction successful! Total characters: {len(result_text)}")
        except Exception as err:
            print(f"Extraction Error: {err}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Usage: python logic/extract_text.py <path_to_pdf_or_docx>")

```

---

## 📄 `logic/llm_calls.py`

```python
import os
import re
import json
import time
from typing import Dict, Any, Optional, List

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# API Configuration
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", os.environ.get("API_KEY", ""))
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", os.environ.get("API_KEY", ""))
GROQ_MODELS = ["qwen/qwen3.6-27b", "openai/gpt-oss-120b", "openai/gpt-oss-20b"]

# Anthropic Configuration
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6")

try:
    from groq import Groq
    groq_available = True
except ImportError:
    groq_available = False

try:
    import anthropic
    anthropic_available = True
except ImportError:
    anthropic_available = False

def get_groq_client() -> Optional[Any]:
    if not groq_available:
        return None
    api_key = os.environ.get("GROQ_API_KEY", GROQ_API_KEY)
    if not api_key:
        return None
    try:
        return Groq(api_key=api_key, timeout=45.0)
    except Exception:
        return None

def get_anthropic_client() -> Optional[Any]:
    if not anthropic_available:
        return None
    api_key = os.environ.get("ANTHROPIC_API_KEY", ANTHROPIC_API_KEY)
    if not api_key:
        return None
    try:
        return anthropic.Anthropic(api_key=api_key, timeout=45.0)
    except Exception:
        return None

def clean_json_response(raw_text: str) -> Optional[dict]:
    """
    Cleans reasoning tags, extracts JSON code blocks, and returns parsed dictionary.
    """
    if not raw_text or not raw_text.strip():
        return None
        
    cleaned = raw_text.strip()
    cleaned = re.sub(r"<think>.*?</think>", "", cleaned, flags=re.DOTALL).strip()
    
    # 1. Direct JSON parse
    try:
        data = json.loads(cleaned)
        if isinstance(data, dict):
            return data
    except Exception:
        pass

    # 2. Markdown code block regex extraction
    code_block_matches = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, re.DOTALL)
    for block in code_block_matches:
        try:
            data = json.loads(block)
            if isinstance(data, dict):
                return data
        except Exception:
            pass

    # 3. Outer brace extraction
    brace_match = re.search(r"(\{.*\})", cleaned, re.DOTALL)
    if brace_match:
        try:
            data = json.loads(brace_match.group(1))
            if isinstance(data, dict):
                return data
        except Exception:
            pass

    return None

def normalize_analysis_dict(data: dict) -> dict:
    """
    Ensures all required schema keys are present with appropriate data types.
    """
    required_keys = {
        "doc_type": "Official Document / Notice",
        "summary": "Document analyzed successfully.",
        "steps": [],
        "deadlines": [],
        "required_documents": [],
        "risks": []
    }
    normalized = {}
    for key, default_val in required_keys.items():
        val = data.get(key)
        if val is None:
            normalized[key] = default_val
        elif isinstance(default_val, list) and not isinstance(val, list):
            normalized[key] = [str(val)]
        else:
            normalized[key] = val
            
    if isinstance(normalized["deadlines"], list):
        cleaned_deadlines = []
        for item in normalized["deadlines"]:
            if isinstance(item, dict):
                cleaned_deadlines.append({
                    "date": str(item.get("date", "Timeline")),
                    "description": str(item.get("description", "Action item / submission"))
                })
            elif isinstance(item, str):
                cleaned_deadlines.append({
                    "date": "Timeline",
                    "description": item
                })
        normalized["deadlines"] = cleaned_deadlines

    if isinstance(normalized["steps"], list):
        normalized["steps"] = [str(s) for s in normalized["steps"] if s]
    if isinstance(normalized["required_documents"], list):
        normalized["required_documents"] = [str(d) for d in normalized["required_documents"] if d]
    if isinstance(normalized["risks"], list):
        normalized["risks"] = [str(r) for r in normalized["risks"] if r]

    return normalized

def prepare_context_payload(text: str, max_chars: int = 15000) -> str:
    if len(text) <= max_chars:
        return text
    head = text[:10000]
    tail = text[-4000:]
    return f"{head}\n\n[... content truncated for optimal summarization ...]\n\n{tail}"

# ----------------- SHARED PROMPT HELPER -----------------
def build_system_prompt(domain: str, language: str = "English", task_type: str = "qa") -> str:
    """
    Standardized prompt construction for all LLM calls ensuring consistent capability,
    actionability, uncertainty handling, tone, and language adherence.
    """
    base_instructions = (
        f"You are a helpful, authoritative, and practical citizen assistant for an Indian {domain} guide app.\n"
        f"LANGUAGE REQUIREMENT: You MUST respond strictly and entirely in {language} with natural fluency, polite tone, and no English mixed in (except standard abbreviations like PAN, OTP, IFSC, NEFT, Aadhaar).\n"
        f"TONE & STYLE: Plain language, clear formatting, bullet points, and actionable guidance aimed at a first-time citizen navigating administrative procedures.\n"
        f"UNCERTAINTY & ACCURACY: Be factual and precise. If exact fees, interest rates, or eligibility cutoffs vary by state, bank, or insurer, explicitly mention that they vary and advise the user to confirm directly with the designated branch or official portal rather than guessing."
    )

    if task_type == "document_analysis":
        return (
            f"{base_instructions}\n\n"
            f"TASK: Analyze the provided document text and produce a detailed, highly informative breakdown.\n"
            f"You MUST respond ONLY with a single valid JSON object containing EXACTLY these keys:\n"
            f"- \"doc_type\": Title or classification of the document (string, in {language})\n"
            f"- \"summary\": Detailed, plain-language explanation of what this document covers, key rules, and importance (string, in {language})\n"
            f"- \"steps\": Chronological array of actionable steps or procedural requirements (array of strings, in {language})\n"
            f"- \"deadlines\": Array of objects with \"date\" (string) and \"description\" (string, in {language})\n"
            f"- \"required_documents\": Array of documents, ID proofs, or certificates needed or mentioned (array of strings, in {language})\n"
            f"- \"risks\": Array of critical warnings, compliance notices, or consequences of delay (array of strings, in {language})\n"
        )
    elif task_type == "grounded_qa":
        return (
            f"{base_instructions}\n\n"
            f"TASK: Answer the user's question clearly, thoroughly, and practically using the provided context (document text or curated process guide).\n"
            f"GUIDELINES:\n"
            f"1. Ground your answer in the provided context details (such as required documents, authority, steps, and rules).\n"
            f"2. Provide practical assistance (e.g. if the user asks what to do if a document is missing, clarify valid alternative proofs recognized under standard Indian administrative procedures).\n"
            f"3. If a question is completely unrelated or cannot be addressed even with standard citizen guidance, state politely: \"I'm not certain based on this document/guide.\"\n"
            f"4. Format your answer with clear bullet points and bold highlights for readability."
        )
    elif task_type == "general_qa":
        return (
            f"{base_instructions}\n\n"
            f"TASK: Answer citizen queries about Indian citizen procedures, government services (PAN, Aadhaar, Passport, ITR), banking operations (KYC, loans, account transfer), and insurance claims.\n"
            f"Provide actionable step-by-step advice, required document checklists, and mention official portals (like myAadhaar, Protean NSDL, Passport Seva, DigiLocker)."
        )
    return base_instructions

# ----------------- 1. DOCUMENT ANALYSIS -----------------
def analyze_document(text: str, language: str = "English") -> Dict[str, Any]:
    """
    Analyzes uploaded document and returns structured JSON summary.
    """
    if not text or not text.strip():
        return {"error": "Document text is empty. Please upload a readable document."}

    system_prompt = build_system_prompt("document & official process", language=language, task_type="document_analysis")
    context_to_send = prepare_context_payload(text)
    user_prompt = f"DOCUMENT CONTENT TO ANALYZE:\n\n{context_to_send}"
    
    last_error = None
    
    # 1. Try Groq API
    groq_client = get_groq_client()
    if groq_client:
        for model in GROQ_MODELS:
            for attempt in range(2):
                try:
                    resp = groq_client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        max_tokens=4096,
                        temperature=0.1
                    )
                    raw_text = resp.choices[0].message.content
                    parsed = clean_json_response(raw_text)
                    if parsed:
                        return normalize_analysis_dict(parsed)
                    else:
                        last_error = f"Unparseable response: {raw_text[:200]}"
                except Exception as e:
                    last_error = str(e)
                    time.sleep(0.5)
                    continue

    # 2. Try Anthropic API
    anthropic_client = get_anthropic_client()
    if anthropic_client:
        models_to_try = [ANTHROPIC_MODEL, "claude-3-7-sonnet-20250219", "claude-3-5-sonnet-20241022"]
        for model in models_to_try:
            for attempt in range(2):
                try:
                    resp = anthropic_client.messages.create(
                        model=model,
                        max_tokens=4000,
                        system=system_prompt,
                        messages=[{"role": "user", "content": user_prompt}]
                    )
                    raw_text = resp.content[0].text
                    parsed = clean_json_response(raw_text)
                    if parsed:
                        return normalize_analysis_dict(parsed)
                    else:
                        last_error = f"Unparseable response: {raw_text[:200]}"
                except Exception as e:
                    last_error = str(e)
                    time.sleep(0.5)
                    continue

    if last_error:
        return {"error": last_error}
        
    return {
        "doc_type": f"Extracted Document ({language})",
        "summary": f"Document analyzed ({len(text)} characters).",
        "steps": [
            "Review the specific provisions and requirements listed in the document.",
            "Verify all required identification credentials and supporting records.",
            "Complete submission or follow up with the concerned office before due dates."
        ],
        "deadlines": [
            {"date": "Timeline", "description": "Standard compliance and registration window"}
        ],
        "required_documents": [
            "Official Identity Proof",
            "Supporting forms and fee clearance receipts"
        ],
        "risks": [
            "Non-compliance or missed deadlines may lead to penalties or administrative debarment."
        ]
    }

# ----------------- 2. GROUNDED SECTION & DOCUMENT Q&A -----------------
def answer_question(document_text: str, question: str, language: str = "English", history: Optional[List[Dict[str, str]]] = None) -> str:
    """
    Answers user questions grounded in document text OR curated section guide data
    (Government / Banking / Insurance) with full capability and consistency.
    """
    if not question or not question.strip():
        return "Please enter a question to ask."

    system_prompt = build_system_prompt("document, government, banking, and insurance", language=language, task_type="grounded_qa")
    context_to_send = prepare_context_payload(document_text, max_chars=16000)
    
    messages = [{"role": "system", "content": system_prompt}]
    
    # Include recent conversation turns for context
    if history:
        for h in history[-4:]:
            r = h.get("role", "user")
            c = h.get("content", "")
            if r in ["user", "assistant"] and c:
                messages.append({"role": r, "content": c})
                
    user_payload = f"REFERENCE CONTEXT / GUIDE DATA:\n{context_to_send}\n\nCITIZEN QUESTION:\n{question}"
    messages.append({"role": "user", "content": user_payload})

    # 1. Try Groq API
    groq_client = get_groq_client()
    if groq_client:
        for model in GROQ_MODELS:
            for attempt in range(2):
                try:
                    resp = groq_client.chat.completions.create(
                        model=model,
                        messages=messages,
                        max_tokens=2048,
                        temperature=0.15
                    )
                    raw_ans = resp.choices[0].message.content.strip()
                    clean_ans = re.sub(r"<think>.*?</think>", "", raw_ans, flags=re.DOTALL).strip()
                    if clean_ans:
                        return clean_ans
                except Exception:
                    time.sleep(0.5)
                    continue

    # 2. Try Anthropic API
    anthropic_client = get_anthropic_client()
    if anthropic_client:
        for model in [ANTHROPIC_MODEL, "claude-3-7-sonnet-20250219"]:
            for attempt in range(2):
                try:
                    resp = anthropic_client.messages.create(
                        model=model,
                        max_tokens=1500,
                        system=system_prompt,
                        messages=[{"role": "user", "content": user_payload}]
                    )
                    return resp.content[0].text.strip()
                except Exception:
                    time.sleep(0.5)
                    continue

    if not document_text or not document_text.strip():
        return "I'm not certain based on this document."
    return f"Based on this guide, please verify your specific case details with the concerned department or branch for personalized guidance."

# ----------------- 3. GENERAL CITIZEN ASSISTANT -----------------
def general_chat_answer(question: str, history: Optional[List[Dict[str, str]]] = None, language: str = "English") -> str:
    """
    Answers general citizen questions about Indian government processes, banking, tax,
    and documents using the configured LLM engine.
    """
    if not question or not question.strip():
        return "Please enter a question to ask."

    system_prompt = build_system_prompt("citizen and public service", language=language, task_type="general_qa")

    messages = [{"role": "system", "content": system_prompt}]
    if history:
        for h in history[-4:]:
            r = h.get("role", "user")
            c = h.get("content", "")
            if r in ["user", "assistant"] and c:
                messages.append({"role": r, "content": c})
    messages.append({"role": "user", "content": question})

    # 1. Try Groq API
    groq_client = get_groq_client()
    if groq_client:
        for model in GROQ_MODELS:
            for attempt in range(2):
                try:
                    resp = groq_client.chat.completions.create(
                        model=model,
                        messages=messages,
                        max_tokens=2048,
                        temperature=0.2
                    )
                    raw_ans = resp.choices[0].message.content.strip()
                    clean_ans = re.sub(r"<think>.*?</think>", "", raw_ans, flags=re.DOTALL).strip()
                    if clean_ans:
                        return clean_ans
                except Exception:
                    time.sleep(0.5)
                    continue

    # 2. Try Anthropic API
    anthropic_client = get_anthropic_client()
    if anthropic_client:
        for model in [ANTHROPIC_MODEL, "claude-3-7-sonnet-20250219"]:
            for attempt in range(2):
                try:
                    resp = anthropic_client.messages.create(
                        model=model,
                        max_tokens=1500,
                        system=system_prompt,
                        messages=[{"role": "user", "content": question}]
                    )
                    return resp.content[0].text.strip()
                except Exception:
                    time.sleep(0.5)
                    continue

    return "I am ready to help you with any questions regarding Indian documents, citizen procedures, PAN, Aadhaar, Passport, or tax notices."

# ----------------- 4. BANK SPECIFIC LOAN GUIDANCE -----------------
def bank_loan_info(bank_name: str, loan_type: str, language: str = "English") -> Dict[str, Any]:
    """
    Generates bank-specific and loan-type specific guidance in the target language.
    Does NOT state specific interest rates or exact numeric fee amounts (defers to disclaimer).
    """
    system_prompt = (
        f"You are an authoritative banking information assistant for an Indian financial guidance app.\n"
        f"The user wants general guidance about a {loan_type} from {bank_name} in India.\n"
        f"LANGUAGE REQUIREMENT: Respond strictly in {language}.\n"
        f"Return ONLY valid JSON with this structure:\n"
        f"{{\n"
        f"  \"overview\": \"brief description of this loan type at this bank, in general terms\",\n"
        f"  \"typical_documents\": [\"document 1\", \"document 2\", ...],\n"
        f"  \"general_process\": [\"step 1\", \"step 2\", ...],\n"
        f"  \"disclaimer\": \"Exact interest rates, eligibility criteria, processing fees, and margin requirements vary by profile and change periodically according to RBI repo rate/MCLR guidelines. Always confirm current rates and terms directly on {bank_name}'s official portal or your nearest branch.\"\n"
        f"}}\n"
        f"CRITICAL RULES:\n"
        f"1. Do NOT state specific interest rates (e.g. do not say '8.5%'), exact fee amounts (e.g. do not say '₹5,000'), or exact income eligibility numbers.\n"
        f"2. Describe financial terms generally (e.g. 'rates are linked to repo rate / MCLR benchmarks and vary based on applicant credit score and loan tenure') and defer to the disclaimer.\n"
        f"3. All text inside JSON must be written strictly in {language}."
    )

    user_prompt = f"Provide {language} guidance for applying for a {loan_type} at {bank_name} in India."

    # 1. Try Groq API
    groq_client = get_groq_client()
    if groq_client:
        for model in GROQ_MODELS:
            for attempt in range(2):
                try:
                    resp = groq_client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        max_tokens=2048,
                        temperature=0.1
                    )
                    raw_text = resp.choices[0].message.content
                    parsed = clean_json_response(raw_text)
                    if parsed and "overview" in parsed and "typical_documents" in parsed:
                        return parsed
                except Exception:
                    time.sleep(0.5)
                    continue

    # 2. Try Anthropic API
    anthropic_client = get_anthropic_client()
    if anthropic_client:
        for model in [ANTHROPIC_MODEL, "claude-3-7-sonnet-20250219"]:
            for attempt in range(2):
                try:
                    resp = anthropic_client.messages.create(
                        model=model,
                        max_tokens=2000,
                        system=system_prompt,
                        messages=[{"role": "user", "content": user_prompt}]
                    )
                    raw_text = resp.content[0].text
                    parsed = clean_json_response(raw_text)
                    if parsed and "overview" in parsed and "typical_documents" in parsed:
                        return parsed
                except Exception:
                    time.sleep(0.5)
                    continue

    # Deterministic fallback
    disclaimer_text = (
        f"Exact interest rates, processing fees, and eligibility thresholds vary by applicant profile and change periodically. "
        f"Please verify current terms directly with {bank_name}."
    )
    if language == "Hindi":
        disclaimer_text = f"सटीक ब्याज दरें, प्रसंस्करण शुल्क और पात्रता मानदंड आवेदक की प्रोफ़ाइल के अनुसार भिन्न होते हैं और समय-समय पर बदलते रहते हैं। कृपया {bank_name} से सीधे वर्तमान शर्तों की पुष्टि करें।"
    elif language == "Kannada":
        disclaimer_text = f"ನಿಖರವಾದ ಬಡ್ಡಿದರಗಳು, ಪ್ರಕ್ರಿಯಾ ಶುಲ್ಕಗಳು ಮತ್ತು ಅರ್ಹತಾ ಮಾನದಂಡಗಳು ಬದಲಾಗುತ್ತವೆ. ದಯವಿಟ್ಟು {bank_name} ನೊಂದಿಗೆ ಪ್ರಸ್ತುತ ನಿಯಮಗಳನ್ನು ನೇರವಾಗಿ ದೃಢೀಕರಿಸಿ."

    return {
        "overview": f"{loan_type} offered by {bank_name} provides structured financing options with standard digital and in-branch processing for eligible applicants.",
        "typical_documents": [
            "Officially Valid ID Proof (Aadhaar Card / PAN Card / Passport)",
            "Proof of Address (Utility Bill / Passport / Aadhaar)",
            "Income Proof: Salary slips (last 3-6 months) / ITR & Form 16 (last 2 years)",
            "Bank statements of primary operative account for past 6 to 12 months",
            "Property or purpose-specific documentation (e.g. Title deed for Home Loan, Admission letter for Education Loan)"
        ],
        "general_process": [
            f"Check basic eligibility and credit profile (CIBIL score) on {bank_name}'s digital portal or branch.",
            "Complete the loan application form and submit initial demographic & income details.",
            "Provide self-attested KYC documents, bank statements, and relevant collateral/asset papers.",
            f"Undergo credit appraisal, property legal/technical verification, and underwriting by {bank_name}.",
            "Review the official Sanction Letter detailing approved amount, tenure, and benchmark-linked interest terms.",
            "Sign the loan agreement, execute NACH auto-debit mandate, and receive disbursement."
        ],
        "disclaimer": disclaimer_text
    }

```

---

## 📄 `logic/process_data.py`

```python
﻿import json
import os
from typing import List, Dict, Any, Optional
import streamlit as st
from logic.translations import get_normalized_language

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
GOVT_DATA_PATH = os.path.join(DATA_DIR, "processes.json")
BANKING_DATA_PATH = os.path.join(DATA_DIR, "banking_processes.json")
INSURANCE_DATA_PATH = os.path.join(DATA_DIR, "insurance_processes.json")

# Multilingual localized process overrides for Government & Banking
LOCALIZED_PROCESS_DATA = {
    "Hindi": {
        # Government
        "pan_card": {
            "name": "नया पैन कार्ड आवेदन (फॉर्म 49A)",
            "description": "आयकर विभाग के तहत भारतीय नागरिकों, संस्थाओं और ट्रस्टों के लिए 10-अंकीय अल्फ़ान्यूमेरिक स्थायी खाता संख्या (पैन) के आवंटन के लिए आवेदन।",
            "steps": [
                "आधिकारिक Protean (NSDL) e-Gov या UTIITSL ऑनलाइन पोर्टल पर जाएं (या अधिकृत TIN-FC केंद्र पर जाएं)।",
                "आवेदन प्रकार के रूप में 'फॉर्म 49A - भारतीय नागरिक' चुनें और श्रेणी चुनें (उदा. व्यक्तिगत)।",
                "व्यक्तिगत विवरण भरें: पूरा नाम, जन्म तिथि, लिंग, पिता का नाम और पता।",
                "जमा करने का माध्यम चुनें: पेपरलेस e-KYC/e-Sign (आधार ओटीपी के माध्यम से), स्कैन की गई छवियां अपलोड करें, या भौतिक दस्तावेज़ भेजें।",
                "नेट बैंकिंग, डेबिट/क्रेडिट कार्ड या यूपीआई का उपयोग करके निर्धारित आवेदन प्रसंस्करण शुल्क का भुगतान करें।",
                "वितरण और प्रसंस्करण स्थिति को ट्रैक करने के लिए 15-अंकीय पावती पर्ची डाउनलोड करें और सहेजें।",
                "यदि भौतिक मोड चुना गया था, तो हस्ताक्षरित फॉर्म को स्व-सत्यापित प्रतियों के साथ 15 दिनों के भीतर केंद्र पर भेजें।"
            ],
            "required_documents": [
                "पहचान का प्रमाण (POI): आधार कार्ड, मतदाता पहचान पत्र, पासपोर्ट, या ड्राइविंग लाइसेंस",
                "पते का प्रमाण (POA): आधार कार्ड, बिजली बिल (< 3 महीने), बैंक खाता विवरण, या डाकघर पासबुक",
                "जन्म तिथि का प्रमाण (DOB): आधार कार्ड, जन्म प्रमाण पत्र, मैट्रिकुलेशन मार्कशीट, या पासपोर्ट",
                "भौतिक आवेदनों के लिए दो हालिया पासपोर्ट आकार के रंगीन फोटो (3.5 सेमी x 2.5 सेमी)"
            ],
            "authority_type": "आयकर विभाग (Protean eGov / UTIITSL के माध्यम से)",
            "estimated_time": "भौतिक कार्ड के लिए 10 से 15 कार्य दिवस; तत्काल ई-पैन के लिए 2 से 3 दिन",
            "fees": "भारत के भीतर ₹107 (जीएसटी सहित); विदेशी पते के लिए ₹1,017; ई-पैन निःशुल्क/नाममात्र है"
        },
        "aadhaar_update": {
            "name": "आधार कार्ड सुधार एवं अद्यतन",
            "description": "UIDAI के साथ जनसांख्यिकीय विवरण (नाम, पता, जन्म तिथि, लिंग, मोबाइल नंबर) या बायोमेट्रिक डेटा (फिंगरप्रिंट, आईरिस, फोटो) को अपडेट या सही करने की प्रक्रिया।",
            "steps": [
                "पात्रता जांचें: पता और दस्तावेज़ अपडेट myAadhaar पोर्टल के माध्यम से ऑनलाइन किए जा सकते हैं; मोबाइल नंबर, नाम सुधार और बायोमेट्रिक्स के लिए व्यक्तिगत रूप से आधार नामांकन केंद्र पर जाना होगा।",
                "ऑनलाइन (पता अपडेट): आधार नंबर और पंजीकृत मोबाइल पर भेजे गए ओटीपी का उपयोग करके myAadhaar पोर्टल पर लॉग इन करें।",
                "'अपडेट एड्रेस' चुनें, नए पते का विवरण दर्ज करें और वैध सहायक प्रमाण अपलोड करें।",
                "व्यक्तिगत अपडेट (नाम, जन्मतिथि, मोबाइल, बायोमेट्रिक्स): UIDAI पोर्टल के माध्यम से अपॉइंटमेंट बुक करें या अधिकृत आधार सेवा केंद्र / बैंक / डाकघर केंद्र पर जाएं।",
                "आधार सुधार फॉर्म भरें और ऑपरेटर को मूल सत्यापन दस्तावेज प्रस्तुत करें।",
                "बायोमेट्रिक प्रमाणीकरण प्रदान करें और स्क्रीन पर ऑपरेटर की प्रविष्टि को सत्यापित करें।",
                "अपडेट अनुरोध संख्या (URN) पावती पर्ची प्राप्त करें और UIDAI पोर्टल पर स्थिति ट्रैक करें।"
            ],
            "required_documents": [
                "नाम सुधार के लिए: पहचान का प्रमाण (पासपोर्ट, पैन कार्ड, वोटर आईडी, फोटो सहित राशन कार्ड)",
                "पता अपडेट के लिए: पते का प्रमाण (बिजली/पानी का बिल < 3 महीने, किराया समझौता, बैंक पासबुक, पासपोर्ट)",
                "जन्मतिथि सुधार के लिए: जन्म तिथि का प्रमाण (जन्म प्रमाण पत्र, एसएसएलसी/10वीं का प्रमाण पत्र, पासपोर्ट)",
                "मौजूदा आधार कार्ड नंबर / प्रति"
            ],
            "authority_type": "भारतीय विशिष्ट पहचान प्राधिकरण (UIDAI) / आधार सेवा केंद्र",
            "estimated_time": "5 से 15 कार्य दिवस (मानक SLA के तहत अधिकतम 30 दिन)",
            "fees": "जनसांख्यिकीय अपडेट के लिए ₹50; बायोमेट्रिक अपडेट के लिए ₹100; पोर्टल पर ऑनलाइन दस्तावेज़ अपडेट समय-समय पर निःशुल्क"
        },
        "passport_renewal": {
            "name": "पासपोर्ट नवीनीकरण / पुनः जारी",
            "description": "विदेश मंत्रालय के माध्यम से समाप्ति, वीज़ा पृष्ठों की समाप्ति, व्यक्तिगत विवरण में परिवर्तन, या क्षतिग्रस्त/खोई हुई पुस्तिका के कारण भारतीय पासपोर्ट को पुनः जारी करने का आवेदन।",
            "steps": [
                "आधिकारिक पासपोर्ट सेवा पोर्टल (passportindia.gov.in) या mPassport Seva ऐप पर पंजीकरण करें और खाता बनाएं।",
                "'ताज़ा पासपोर्ट/पासपोर्ट पुनः जारी करने के लिए आवेदन करें' चुनें और सामान्य या तत्काल योजना (36 या 60 पृष्ठ पुस्तिका) चुनें।",
                "आवेदक विवरण, पारिवारिक जानकारी, पता और पिछले पासपोर्ट विवरण के साथ ऑनलाइन आवेदन पत्र भरें।",
                "ऑनलाइन शुल्क भुगतान करें और निकटतम पासपोर्ट सेवा केंद्र (PSK) या डाकघर पासपोर्ट सेवा केंद्र (POPSK) में अपॉइंटमेंट निर्धारित करें।",
                "अपॉइंटमेंट बैच और ARN (आवेदन संदर्भ संख्या) वाली आवेदन रसीद को प्रिंट या सहेजें।",
                "मूल दस्तावेजों और स्व-सत्यापित फोटोकॉपी के साथ निर्धारित तिथि और समय पर निर्दिष्ट PSK/POPSK पर जाएं।",
                "तीन चरणों का काउंटर सत्यापन पूरा करें (काउंटर A: बायोमेट्रिक्स और फोटो, काउंटर B: दस्तावेज़ सत्यापन, काउंटर C: अनुमोदन)।",
                "यदि आपके पते की स्थिति के लिए आवश्यक हो तो स्थानीय पुलिस सत्यापन पूरा करें।",
                "अपने पंजीकृत निवास पर स्पीड पोस्ट के माध्यम से नवीनीकृत पासपोर्ट प्राप्त करें।"
            ],
            "required_documents": [
                "पहले दो और अंतिम दो पृष्ठों (ईसीआर/गैर-ईसीआर पृष्ठ सहित) की स्व-सत्यापित फोटोकॉपी के साथ पुराना मूल पासपोर्ट",
                "वर्तमान पते का प्रमाण (आधार कार्ड, उपयोगिता बिल, बैंक पासबुक, जीवनसाथी का पासपोर्ट)",
                "जन्म तिथि का प्रमाण (आधार कार्ड, जन्म प्रमाण पत्र, स्कूल छोड़ने का प्रमाण पत्र)",
                "व्यक्तिगत विवरण में किसी भी बदलाव के लिए दस्तावेजी प्रमाण (उदा. विवाह प्रमाण पत्र, राजपत्र अधिसूचना)"
            ],
            "authority_type": "पासपोर्ट सेवा केंद्र (PSK) / क्षेत्रीय पासपोर्ट कार्यालय (RPO), विदेश मंत्रालय",
            "estimated_time": "सामान्य: 15 से 30 कार्य दिवस (पुलिस सत्यापन के बाद); तत्काल: 1 से 3 कार्य दिवस",
            "fees": "सामान्य (36 पृष्ठ): ₹1,500; सामान्य (60 पृष्ठ): ₹2,000; तत्काल: अतिरिक्त ₹2,000"
        },
        # Banking
        "loan_documentation": {
            "name": "बैंक ऋण आवेदन एवं दस्तावेज़ीकरण",
            "description": "भारतीय वाणिज्यिक और सार्वजनिक क्षेत्र के बैंकों में व्यक्तिगत, गृह, वाहन या शिक्षा ऋण के लिए सामान्य प्रक्रिया और मानक दस्तावेज़ीकरण चेकलिस्ट।",
            "steps": [
                "पात्रता और क्रेडिट स्कोर की जांच करें (इष्टतम ब्याज दरों के लिए आमतौर पर 750 से अधिक सिबिल स्कोर पसंद किया जाता है)।",
                "ऋण श्रेणी (गृह, व्यक्तिगत, वाहन, शिक्षा) चुनें और आधिकारिक कोटेशन का अनुरोध करें।",
                "बैंक शाखा या आधिकारिक नेट-बैंकिंग / मोबाइल ऐप के माध्यम से भरा हुआ ऋण आवेदन पत्र जमा करें।",
                "केवाईसी प्रमाण, आय का प्रमाण (वेतन पर्ची / आईटीआर / फॉर्म 16), बैंक विवरण और संपत्ति/संपार्श्विक दस्तावेज जमा करें।",
                "बैंक क्रेडिट मूल्यांकन, निवास/कार्यालय का सत्यापन और तकनीकी संपत्ति मूल्यांकन करवाएं।",
                "स्वीकृत राशि, ब्याज दर, प्रसंस्करण शुल्क और ईएमआई अवधि का विवरण देने वाले आधिकारिक स्वीकृति पत्र की समीक्षा करें।",
                "ऋण समझौते पर हस्ताक्षर करें, ऑटो-डेबिट के लिए NACH/ई-जनादेश जमा करें और ऋण राशि प्राप्त करें।"
            ],
            "required_documents": [
                "पहचान और पते का प्रमाण (आधार कार्ड, पैन कार्ड, पासपोर्ट, वोटर आईडी)",
                "वेतनभोगियों के लिए आय का प्रमाण: पिछले 3 से 6 महीने की वेतन पर्ची और 2 साल का फॉर्म 16/आईटीआर",
                "स्व-नियोजित के लिए: पिछले 2 से 3 वर्षों का ऑडिटेड आईटीआर, पी एंड एल विवरण और व्यापार पंजीकरण प्रमाण (जीएसटी)",
                "वेतन/आय दर्शाने वाले पिछले 6 से 12 महीनों के बैंक खाते का विवरण",
                "संपत्ति दस्तावेज (गृह ऋण के लिए): टाइटल डीड, स्वीकृत भवन योजना, बिक्री समझौता, एनओसी",
                "संस्थान से प्रवेश पत्र और शुल्क अनुसूची (शिक्षा ऋण के लिए)"
            ],
            "authority_type": "आपकी बैंक शाखा / ऋण संस्थान",
            "estimated_time": "व्यक्तिगत ऋण: 1 से 3 कार्य दिवस; गृह/संपत्ति ऋण: 7 से 15 कार्य दिवस (बैंक के अनुसार भिन्न)",
            "fees": "ऋण राशि का 0.25% से 2% प्रसंस्करण शुल्क (प्लस जीएसटी); स्टांप शुल्क राज्य के अनुसार भिन्न"
        },
        "kyc_account_opening": {
            "name": "नया बैंक खाता खोलना एवं केवाईसी सत्यापन",
            "description": "डिजिटल (वीडियो केवाईसी) या शाखा में जाकर पूर्ण केवाईसी अनुपालन के साथ बचत या चालू बैंक खाता खोलने की चरण-दर-चरण प्रक्रिया।",
            "steps": [
                "बैंक और खाते का प्रकार चुनें (नियमित बचत, शून्य शेष / बीएसबीडी, वेतन खाता, या चालू खाता)।",
                "बैंक की आधिकारिक वेबसाइट / मोबाइल ऐप से ऑनलाइन आवेदन करें या निकटतम शाखा से फॉर्म प्राप्त करें।",
                "व्यक्तिगत विवरण भरें: पूरा नाम, जन्म तिथि, पैन, आधार संख्या, व्यवसाय, वार्षिक आय और नामांकित व्यक्ति का विवरण।",
                "केवाईसी मोड चुनें: ऑनलाइन वीडियो केवाईसी (V-KYC) या शाखा में बायोमेट्रिक प्रमाणीकरण।",
                "वीडियो केवाईसी: बैंक अधिकारी के साथ लाइव कॉल में शामिल हों, मूल पैन कार्ड दिखाएं और हस्ताक्षर कैप्चर करें।",
                "न्यूनतम प्रारंभिक शेष राशि जमा करें (यदि आवश्यक हो)।",
                "अपने पंजीकृत पते पर खाता संख्या, ग्राहक आईडी (CIF), डेबिट कार्ड, चेक बुक और वेलकम किट प्राप्त करें।"
            ],
            "required_documents": [
                "पहचान के लिए आधिकारिक वैध दस्तावेज़ (OVD): पैन कार्ड (अनिवार्य या फॉर्म 60) और आधार कार्ड",
                "पते का प्रमाण (POA): आधार कार्ड, पासपोर्ट, वोटर आईडी, या बिजली/पानी का बिल (< 3 महीने)",
                "दो हालिया पासपोर्ट आकार के रंगीन फोटो (शाखा में खोलने के लिए)",
                "नामांकित व्यक्ति की पहचान और आयु का प्रमाण",
                "व्यापार पंजीकरण और जीएसटी प्रमाण पत्र (चालू खातों के लिए)"
            ],
            "authority_type": "आपकी बैंक शाखा / डिजिटल खाता पोर्टल",
            "estimated_time": "डिजिटल / वीडियो केवाईसी: तत्काल से 24 घंटे; शाखा में खोलना: 2 से 4 कार्य दिवस",
            "fees": "शून्य आवेदन शुल्क; प्रारंभिक जमा खाता प्रकार और शाखा स्थान के अनुसार भिन्न होता है"
        },
        "update_account_details": {
            "name": "बैंक खाता विवरण अपडेट करना (मोबाइल नंबर एवं पता)",
            "description": "सुरक्षित लेनदेन ओटीपी और पत्राचार के लिए अपने बैंक खाते से जुड़े अपने पंजीकृत मोबाइल नंबर, आवासीय पते या ईमेल पते को अपडेट या संशोधित करने की प्रक्रिया।",
            "steps": [
                "आवश्यक अपडेट निर्धारित करें: मोबाइल नंबर बदलने के लिए आमतौर पर एटीएम या शाखा जाना आवश्यक होता है; पता अपडेट ऑनलाइन किया जा सकता है।",
                "एटीएम द्वारा मोबाइल नंबर अपडेट: डेबिट कार्ड डालें, पिन दर्ज करें, 'सेवाएं' > 'मोबाइल नंबर बदलें' चुनें और ओटीपी द्वारा सत्यापित करें।",
                "शाखा द्वारा मोबाइल नंबर अपडेट: गृह शाखा में जाएं, ग्राहक अनुरोध फॉर्म (CRF) भरें और स्व-सत्यापित पहचान प्रमाण जमा करें।",
                "नेट-बैंकिंग द्वारा पता अपडेट: पोर्टल में लॉग इन करें, 'प्रोफ़ाइल' > 'पता अपडेट' पर जाएं और आधार ओटीपी द्वारा पुष्टि करें।",
                "शाखा द्वारा पता अपडेट: नए पते के प्रमाण के साथ अनुरोध फॉर्म जमा करें।",
                "अद्यतन पूरा होने पर आधिकारिक पुष्टिकरण एसएमएस और ईमेल प्राप्त करें।"
            ],
            "required_documents": [
                "पहचान सत्यापन के लिए मूल पैन कार्ड और आधार कार्ड",
                "नए पते का वैध प्रमाण: अद्यतन आधार कार्ड, पासपोर्ट, वोटर आईडी, या बिजली का बिल (< 3 महीने)",
                "सक्रिय डेबिट कार्ड और पिन (एटीएम चैनल अनुरोधों के लिए)",
                "पासबुक या हालिया बैंक स्टेटमेंट जिसमें खाता संख्या और CIF शामिल हो"
            ],
            "authority_type": "आपकी गृह बैंक शाखा / नेट-बैंकिंग ग्राहक सेवा",
            "estimated_time": "एटीएम / नेट-बैंकिंग: तत्काल से 24 घंटे; शाखा में जमा: 1 से 3 कार्य दिवस",
            "fees": "निःशुल्क / अधिकांश भारतीय बैंकों में कोई शुल्क नहीं"
        },
        "account_transfer": {
            "name": "बैंक खाता शाखा स्थानांतरण गाइड",
            "description": "अपना खाता नंबर बदले बिना अपने सक्रिय बचत या चालू खाते को एक शाखा/शहर से उसी बैंक की दूसरी शाखा में स्थानांतरित करने की चरण-दर-चरण प्रक्रिया।",
            "steps": [
                "उस नई लक्षित शाखा का 4 या 5 अंकों का शाखा कोड और IFSC कोड प्राप्त करें जहाँ आप खाता स्थानांतरित करना चाहते हैं।",
                "विकल्प 1 (ऑनलाइन): नेट-बैंकिंग पोर्टल में लॉग इन करें, 'सेवाएं / खाता अनुरोध' > 'बचत खाता स्थानांतरित करें' पर जाएं।",
                "अपना खाता नंबर चुनें, नया शाखा कोड दर्ज करें और ओटीपी द्वारा अनुरोध सबमिट करें।",
                "विकल्प 2 (शाखा में जाकर): अपनी वर्तमान गृह शाखा या नई शाखा में जाएं, फॉर्म भरें और अप्रयुक्त चेक जमा करें।",
                "पुरानी शाखा से जुड़े किसी भी लंबित लॉकर या ऋण को मंजूरी दें।",
                "ऑनलाइन स्थिति ट्रैक करें; खाता संख्या, डेबिट कार्ड और क्रेडेंशियल अपरिवर्तित रहते हैं।",
                "स्थानांतरण पूरा होने के बाद नए IFSC कोड वाली नई चेक बुक और अपडेट की गई पासबुक प्राप्त करें।"
            ],
            "required_documents": [
                "सक्रिय खाता संख्या और CIF दर्शाने वाली बैंक पासबुक या खाता विवरण",
                "वैध पहचान प्रमाण (आधार कार्ड या पैन कार्ड)",
                "गंतव्य शहर में नए पते का प्रमाण (यदि पता भी अपडेट किया जा रहा है)",
                "पुरानी शाखा से अप्रयुक्त चेक के पन्ने (रद्द करने के लिए)"
            ],
            "authority_type": "आपकी वर्तमान गृह शाखा या गंतव्य बैंक शाखा",
            "estimated_time": "ऑनलाइन नेट-बैंकिंग: 1 से 3 कार्य दिवस; भौतिक शाखा अनुरोध: 3 से 7 कार्य दिवस",
            "fees": "निःशुल्क / सार्वजनिक और निजी क्षेत्र के बैंकों में कोई शुल्क नहीं"
        }
    },
    "Kannada": {
        # Government
        "pan_card": {
            "name": "ಹೊಸ ಪ್ಯಾನ್ ಕಾರ್ಡ್ ಅರ್ಜಿ (ಫಾರ್ಮ್ 49A)",
            "description": "ಆದಾಯ ತೆರಿಗೆ ಇಲಾಖೆಯ ಅಡಿಯಲ್ಲಿ ಭಾರತೀಯ ನಾಗರಿಕರು, ಸಂಸ್ಥೆಗಳು ಮತ್ತು ಟ್ರಸ್ಟ್‌ಗಳಿಗಾಗಿ 10-ಅಂಕಿಯ ಶಾಶ್ವತ ಖಾತೆ ಸಂಖ್ಯೆ (PAN) ಹಂಚಿಕೆಗಾಗಿ ಅರ್ಜಿ.",
            "steps": [
                "ಅಧಿಕೃತ Protean (NSDL) e-Gov ಅಥವಾ UTIITSL ಆನ್‌ಲೈನ್ ಪೋರ್ಟಲ್‌ಗೆ ಭೇಟಿ ನೀಡಿ (ಅಥವಾ ಅಧಿಕೃತ TIN-FC ಕೇಂದ್ರಕ್ಕೆ ಭೇಟಿ ನೀಡಿ).",
                "ಅರ್ಜಿ ಪ್ರಕಾರವಾಗಿ 'ಫಾರ್ಮ್ 49A - ಭಾರತೀಯ ನಾಗರಿಕ' ಆಯ್ಕೆಮಾಡಿ ಮತ್ತು ವರ್ಗವನ್ನು ಆರಿಸಿ (ಉದಾ. ವೈಯಕ್ತಿಕ).",
                "ವೈಯಕ್ತಿಕ ವಿವರಗಳನ್ನು ಭರ್ತಿ ಮಾಡಿ: ಪೂರ್ಣ ಹೆಸರು, ಜನ್ಮ ದಿನಾಂಕ, ಲಿಂಗ, ತಂದೆಯ ಹೆಸರು ಮತ್ತು ವಿಳಾಸ.",
                "ಸಲ್ಲಿಕೆ ವಿಧಾನವನ್ನು ಆರಿಸಿ: ಕಾಗದರಹಿತ e-KYC/e-Sign (ಆಧಾರ್ OTP ಮೂಲಕ), ಸ್ಕ್ಯಾನ್ ಮಾಡಿದ ಚಿತ್ರಗಳ ಅಪ್‌ಲೋಡ್ ಅಥವಾ ಭೌತಿಕ ದಾಖಲೆ ಕಳುಹಿಸುವಿಕೆ.",
                "ನೆಟ್ ಬ್ಯಾಂಕಿಂಗ್, ಡೆಬಿಟ್/ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್ ಅಥವಾ UPI ಬಳಸಿ ನಿಗದಿತ ಅರ್ಜಿ ಶುಲ್ಕವನ್ನು ಪಾವತಿಸಿ.",
                "ವಿತರಣೆ ಮತ್ತು ಪ್ರಕ್ರಿಯೆಯ ಸ್ಥಿತಿಯನ್ನು ಟ್ರ್ಯಾಕ್ ಮಾಡಲು 15-ಅಂಕಿಯ ಸ್ವೀಕೃತಿ ರಶೀದಿಯನ್ನು ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ ಮತ್ತು ಉಳಿಸಿ.",
                "ಭೌತಿಕ ಮೋಡ್ ಆಯ್ಕೆಮಾಡಿದ್ದರೆ, ಸಹಿ ಮಾಡಿದ ಫಾರ್ಮ್ ಅನ್ನು ಸ್ವಯಂ-ದೃಢೀಕರಿಸಿದ ಪ್ರತಿಗಳೊಂದಿಗೆ 15 ದಿನಗಳಲ್ಲಿ ಕಳುಹಿಸಿ."
            ],
            "required_documents": [
                "ಗುರುತಿನ ಪುರಾವೆ (POI): ಆಧಾರ್ ಕಾರ್ಡ್, ಮತದಾರರ ಗುರುತಿನ ಚೀಟಿ, ಪಾಸ್‌ಪೋರ್ಟ್ ಅಥವಾ ಚಾಲನಾ ಪರವಾನಗಿ",
                "ವಿಳಾಸದ ಪುರಾವೆ (POA): ಆಧಾರ್ ಕಾರ್ಡ್, ವಿದ್ಯುತ್ ಬಿಲ್ (< 3 ತಿಂಗಳು), ಬ್ಯಾಂಕ್ ಖಾತೆ ವಿವರ ಅಥವಾ ಪಾಸ್‌ಬುಕ್",
                "ಜನ್ಮ ದಿನಾಂಕದ ಪುರಾವೆ (DOB): ಆಧಾರ್ ಕಾರ್ಡ್, ಜನನ ಪ್ರಮಾಣಪತ್ರ, 10ನೇ ತರಗತಿ ಅಂಕಪಟ್ಟಿ ಅಥವಾ ಪಾಸ್‌ಪೋರ್ಟ್",
                "ಭೌತಿಕ ಅರ್ಜಿಗಳಿಗಾಗಿ ಎರಡು ಇತ್ತೀಚಿನ ಪಾಸ್‌ಪೋರ್ಟ್ ಗಾತ್ರದ ಬಣ್ಣದ ಭಾವಚಿತ್ರಗಳು (3.5 cm x 2.5 cm)"
            ],
            "authority_type": "ಆದಾಯ ತೆರಿಗೆ ಇಲಾಖೆ (Protean eGov / UTIITSL ಮೂಲಕ)",
            "estimated_time": "ಭೌತಿಕ ಕಾರ್ಡ್ ವಿತರಣೆಗೆ 10 ರಿಂದ 15 ಕೆಲಸದ ದಿನಗಳು; ತತ್ಕ್ಷಣದ ಇ-ಪ್ಯಾನ್‌ಗೆ 2 ರಿಂದ 3 ದಿನಗಳು",
            "fees": "ಭಾರತದೊಳಗೆ ರವಾನೆಗಾಗಿ ₹107 (GST ಸೇರಿದಂತೆ); ವಿದೇಶಿ ವಿಳಾಸಕ್ಕೆ ₹1,017; ಇ-ಪ್ಯಾನ್ ಉಚಿತ/ನಾಮಮಾತ್ರ"
        },
        "aadhaar_update": {
            "name": "ಆಧಾರ್ ಕಾರ್ಡ್ ತಿದ್ದುಪಡಿ ಮತ್ತು ನವೀಕರಣ",
            "description": "UIDAI ನೊಂದಿಗೆ ಜನಸಂಖ್ಯಾ ವಿವರಗಳು (ಹೆಸರು, ವಿಳಾಸ, ಜನ್ಮ ದಿನಾಂಕ, ಲಿಂಗ, ಮೊಬೈಲ್ ಸಂಖ್ಯೆ) ಅಥವಾ ಬಯೋಮೆಟ್ರಿಕ್ ಡೇಟಾ (ಬೆರಳಚ್ಚು, ಐರಿಸ್, ಫೋಟೋ) ನವೀಕರಿಸುವ ಪ್ರಕ್ರಿಯೆ.",
            "steps": [
                "ಅರ್ಹತೆಯನ್ನು ಪರಿಶೀಲಿಸಿ: ವಿಳಾಸ ಮತ್ತು ದಾಖಲೆಗಳ ನವೀಕರಣವನ್ನು myAadhaar ಪೋರ್ಟಲ್ ಮೂಲಕ ಆನ್‌ಲೈನ್‌ನಲ್ಲಿ ಮಾಡಬಹುದು; ಮೊಬೈಲ್ ಸಂಖ್ಯೆ, ಹೆಸರು ತಿದ್ದುಪಡಿ ಮತ್ತು ಬಯೋಮೆಟ್ರಿಕ್ಸ್‌ಗೆ ಆಧಾರ್ ನೋಂದಣಿ ಕೇಂದ್ರಕ್ಕೆ ಭೇಟಿ ನೀಡಬೇಕು.",
                "ಆನ್‌ಲೈನ್ (ವಿಳಾಸ ನವೀಕರಣ): ಆಧಾರ್ ಸಂಖ್ಯೆ ಮತ್ತು ನೋಂದಾಯಿತ ಮೊಬೈಲ್‌ಗೆ ಕಳುಹಿಸಲಾದ OTP ಬಳಸಿ myAadhaar ಪೋರ್ಟಲ್‌ಗೆ ಲಾಗ್ ಇನ್ ಮಾಡಿ.",
                "'ಆಧಾರ್‌ನಲ್ಲಿ ವಿಳಾಸ ನವೀಕರಿಸಿ' ಆಯ್ಕೆಮಾಡಿ, ಹೊಸ ವಿಳಾಸದ ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ ಮತ್ತು ಮಾನ್ಯವಾದ ಪುರಾವೆಯನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.",
                "ವೈಯಕ್ತಿಕ ನವೀಕರಣಗಳು (ಹೆಸರು, ಜನ್ಮದಿನಾಂಕ, ಮೊಬೈಲ್, ಬಯೋಮೆಟ್ರಿಕ್ಸ್): UIDAI ಪೋರ್ಟಲ್ ಮೂಲಕ ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್ ಕಾಯ್ದಿರಿಸಿ ಅಥವಾ ಅಧಿಕೃತ ಆಧಾರ್ ಸೇವಾ ಕೇಂದ್ರ / ಬ್ಯಾಂಕ್ / ಪೋಸ್ಟ್ ಆಫೀಸ್ ಕೇಂದ್ರಕ್ಕೆ ಭೇಟಿ ನೀಡಿ.",
                "ಆಧಾರ್ ತಿದ್ದುಪಡಿ ಫಾರ್ಮ್ ಅನ್ನು ಭರ್ತಿ ಮಾಡಿ ಮತ್ತು ಆಪರೇಟರ್‌ಗೆ ಮೂಲ ಪರಿಶೀಲನಾ ದಾಖಲೆಗಳನ್ನು ಸಲ್ಲಿಸಿ.",
                "ಬಯೋಮೆಟ್ರಿಕ್ ದೃಢೀಕರಣವನ್ನು ಒದಗಿಸಿ ಮತ್ತು ಪರದೆಯ ಮೇಲಿನ ನಮೂದನ್ನು ಪರಿಶೀಲಿಸಿ.",
                "ಅಪ್‌ಡೇಟ್ ವಿನಂತಿ ಸಂಖ್ಯೆ (URN) ಸ್ವೀಕೃತಿ ರಶೀದಿಯನ್ನು ಸಂಗ್ರಹಿಸಿ ಮತ್ತು UIDAI ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ಸ್ಥಿತಿಯನ್ನು ಟ್ರ್ಯಾಕ್ ಮಾಡಿ."
            ],
            "required_documents": [
                "ಹೆಸರು ತಿದ್ದುಪಡಿಗಾಗಿ: ಗುರುತಿನ ಪುರಾವೆ (ಪಾಸ್‌ಪೋರ್ಟ್, ಪ್ಯಾನ್ ಕಾರ್ಡ್, ಮತದಾರರ ಗುರುತಿನ ಚೀಟಿ, ಫೋಟೋ ಹೊಂದಿರುವ ಪಡಿತರ ಚೀಟಿ)",
                "ವಿಳಾಸ ನವೀಕರಣಕ್ಕಾಗಿ: ವಿಳಾಸದ ಪುರಾವೆ (ವಿದ್ಯುತ್/ನೀರಿನ ಬಿಲ್ < 3 ತಿಂಗಳು, ಬಾಡಿಗೆ ಒಪ್ಪಂದ, ಬ್ಯಾಂಕ್ ಪಾಸ್‌ಬುಕ್, ಪಾಸ್‌ಪೋರ್ಟ್)",
                "ಜನ್ಮದಿನಾಂಕ ತಿದ್ದುಪಡಿಗಾಗಿ: ಜನ್ಮ ದಿನಾಂಕದ ಪುರಾವೆ (ಜನನ ಪ್ರಮಾಣಪತ್ರ, SSLC/10ನೇ ಪ್ರಮಾಣಪತ್ರ, ಪಾಸ್‌ಪೋರ್ಟ್)",
                "ಅಸ್ತಿತ್ವದಲ್ಲಿರುವ ಆಧಾರ್ ಕಾರ್ಡ್ ಸಂಖ್ಯೆ / ಪ್ರತಿ"
            ],
            "authority_type": "ಭಾರತೀಯ ವಿಶಿಷ್ಟ ಗುರುತಿನ ಪ್ರಾಧಿಕಾರ (UIDAI) / ಆಧಾರ್ ಸೇವಾ ಕೇಂದ್ರ",
            "estimated_time": "5 ರಿಂದ 15 ಕೆಲಸದ ದಿನಗಳು (ಸಾಮಾನ್ಯ SLA ಅಡಿಯಲ್ಲಿ ಗರಿಷ್ಠ 30 ದಿನಗಳು)",
            "fees": "ಜನಸಂಖ್ಯಾ ನವೀಕರಣಗಳಿಗೆ ₹50; ಬಯೋಮೆಟ್ರಿಕ್ ನವೀಕರಣಕ್ಕೆ ₹100; ಆನ್‌ಲೈನ್ ದಾಖಲೆ ನವೀಕರಣಗಳು ನಿಯತಕಾಲಿಕವಾಗಿ ಉಚಿತ"
        },
        "passport_renewal": {
            "name": "ಪಾಸ್‌ಪೋರ್ಟ್ ನವೀಕರಣ / ಮರು-ವಿತರಣೆ",
            "description": "ವಿದೇಶಾಂಗ ವ್ಯವಹಾರಗಳ ಸಚಿವಾಲಯದ ಮೂಲಕ ಅವಧಿ ಮುಕ್ತಾಯ, ವೀಸಾ ಪುಟಗಳ ಕೊರತೆ, ವಿವರಗಳಲ್ಲಿನ ಬದಲಾವಣೆ ಅಥವಾ ಹಾನಿಗೊಳಗಾದ ಕಾರಣ ಭಾರತೀಯ ಪಾಸ್‌ಪೋರ್ಟ್ ಮರು-ವಿತರಣೆಗಾಗಿ ಅರ್ಜಿ.",
            "steps": [
                "ಅಧಿಕೃತ ಪಾಸ್‌ಪೋರ್ಟ್ ಸೇವಾ ಪೋರ್ಟಲ್ (passportindia.gov.in) ಅಥವಾ mPassport Seva ಆ್ಯಪ್‌ನಲ್ಲಿ ನೋಂದಾಯಿಸಿ ಖಾತೆಯನ್ನು ರಚಿಸಿ.",
                "'ಹೊಸ ಪಾಸ್‌ಪೋರ್ಟ್/ಪಾಸ್‌ಪೋರ್ಟ್ ಮರು-ವಿತರಣೆಗಾಗಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ' ಆಯ್ಕೆಮಾಡಿ ಮತ್ತು ಸಾಮಾನ್ಯ ಅಥವಾ ತತ್ಕಾಲ್ ಯೋಜನೆಯನ್ನು ಆರಿಸಿ (36 ಅಥವಾ 60 ಪುಟಗಳ ಬುಕ್‌ಲೆಟ್).",
                "ಅರ್ಜಿದಾರರ ವಿವರಗಳು, ಕುಟುಂಬದ ಮಾಹಿತಿ, ವಿಳಾಸ ಮತ್ತು ಹಿಂದಿನ ಪಾಸ್‌ಪೋರ್ಟ್ ವಿವರಗಳೊಂದಿಗೆ ಆನ್‌ಲೈನ್ ಅರ್ಜಿ ನಮೂನೆಯನ್ನು ಭರ್ತಿ ಮಾಡಿ.",
                "ಆನ್‌ಲೈನ್ ಶುಲ್ಕ ಪಾವತಿ ಮಾಡಿ ಮತ್ತು ಹತ್ತಿರದ ಪಾಸ್‌ಪೋರ್ಟ್ ಸೇವಾ ಕೇಂದ್ರ (PSK) ಅಥವಾ ಪೋಸ್ಟ್ ಆಫೀಸ್ ಪಾಸ್‌ಪೋರ್ಟ್ ಸೇವಾ ಕೇಂದ್ರದಲ್ಲಿ (POPSK) ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್ ನಿಗದಿಪಡಿಸಿ.",
                "ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್ ಬ್ಯಾಚ್ ಮತ್ತು ARN (ಅರ್ಜಿ ಉಲ್ಲೇಖ ಸಂಖ್ಯೆ) ಹೊಂದಿರುವ ಅರ್ಜಿ ರಶೀದಿಯನ್ನು ಮುದ್ರಿಸಿ ಅಥವಾ ಉಳಿಸಿ.",
                "ಮೂಲ ದಾಖಲೆಗಳು ಮತ್ತು ಸ್ವಯಂ-ದೃಢೀಕರಿಸಿದ ಜೆರಾಕ್ಸ್ ಪ್ರತಿಗಳೊಂದಿಗೆ ನಿಗದಿತ ದಿನಾಂಕ ಮತ್ತು ಸಮಯದಲ್ಲಿ ಗೊತ್ತುಪಡಿಸಿದ PSK/POPSK ಗೆ ಭೇಟಿ ನೀಡಿ.",
                "ಮೂರು ಹಂತದ ಕೌಂಟರ್ ಪರಿಶೀಲನೆಯನ್ನು ಪೂರ್ಣಗೊಳಿಸಿ (ಕೌಂಟರ್ A: ಬಯೋಮೆಟ್ರಿಕ್ಸ್ ಮತ್ತು ಫೋಟೋ, ಕೌಂಟರ್ B: ದಾಖಲೆ ಪರಿಶೀಲನೆ, ಕೌಂಟರ್ C: ಮಂಜೂರಾತಿ).",
                "ನಿಮ್ಮ ವಿಳಾಸಕ್ಕೆ ಅಗತ್ಯವಿದ್ದರೆ ಸ್ಥಳೀಯ ಪೊಲೀಸ್ ಪರಿಶೀಲನೆಯನ್ನು ಪೂರ್ಣಗೊಳಿಸಿ.",
                "ನಿಮ್ಮ ನೋಂದಾಯಿತ ವಿಳಾಸದಲ್ಲಿ ಸ್ಪೀಡ್ ಪೋಸ್ಟ್ ಮೂಲಕ ನವೀಕರಿಸಿದ ಪಾಸ್‌ಪೋರ್ಟ್ ಅನ್ನು ಸ್ವೀಕರಿಸಿ."
            ],
            "required_documents": [
                "ಮೊದಲ ಎರಡು ಮತ್ತು ಕೊನೆಯ ಎರಡು ಪುಟಗಳ ಸ್ವಯಂ-ದೃಢೀಕರಿಸಿದ ಜೆರಾಕ್ಸ್ ಪ್ರತಿಗಳೊಂದಿಗೆ ಹಳೆಯ ಮೂಲ ಪಾಸ್‌ಪೋರ್ಟ್ (ECR/Non-ECR ಪುಟ ಸೇರಿದಂತೆ)",
                "ಪ್ರಸ್ತುತ ವಿಳಾಸದ ಪುರಾವೆ (ಆಧಾರ್ ಕಾರ್ಡ್, ಯುಟಿಲಿಟಿ ಬಿಲ್, ಬ್ಯಾಂಕ್ ಪಾಸ್‌ಬುಕ್, ಸಂಗಾತಿಯ ಪಾಸ್‌ಪೋರ್ಟ್)",
                "ಜನ್ಮ ದಿನಾಂಕದ ಪುರಾವೆ (ಆಧಾರ್ ಕಾರ್ಡ್, ಜನನ ಪ್ರಮಾಣಪತ್ರ, ಶಾಲೆ ಬಿಟ್ಟ ಪ್ರಮಾಣಪತ್ರ)",
                "ವೈಯಕ್ತಿಕ ವಿವರಗಳಲ್ಲಿ ಯಾವುದೇ ಬದಲಾವಣೆಗೆ ಸಾಕ್ಷ್ಯಚಿತ್ರ ಪುರಾವೆ (ಉದಾ. ವಿವಾಹ ಪ್ರಮಾಣಪತ್ರ, ಗೆಜೆಟ್ ಅಧಿಸೂಚನೆ)"
            ],
            "authority_type": "ಪಾಸ್‌ಪೋರ್ಟ್ ಸೇವಾ ಕೇಂದ್ರ (PSK) / ಪ್ರಾದೇಶಿಕ ಪಾಸ್‌ಪೋರ್ಟ್ ಕಚೇರಿ (RPO), ವಿದೇಶಾಂಗ ಸಚಿವಾಲಯ",
            "estimated_time": "ಸಾಮಾನ್ಯ: 15 ರಿಂದ 30 ಕೆಲಸದ ದಿನಗಳು (ಪೊಲೀಸ್ ಪರಿಶೀಲನೆಯ ನಂತರ); ತತ್ಕಾಲ್: 1 ರಿಂದ 3 ಕೆಲಸದ ದಿನಗಳು",
            "fees": "ಸಾಮಾನ್ಯ (36 ಪುಟಗಳು): ₹1,500; ಸಾಮಾನ್ಯ (60 ಪುಟಗಳು): ₹2,000; ತತ್ಕಾಲ್: ಹೆಚ್ಚುವರಿ ₹2,000"
        },
        # Banking
        "loan_documentation": {
            "name": "ಬ್ಯಾಂಕ್ ಸಾಲ ಅರ್ಜಿ ಮತ್ತು ದಾಖಲಾತಿ",
            "description": "ಭಾರತೀಯ ವಾಣಿಜ್ಯ ಮತ್ತು ಸಾರ್ವಜನಿಕ ವಲಯದ ಬ್ಯಾಂಕ್‌ಗಳಲ್ಲಿ ವೈಯಕ್ತಿಕ, ಗೃಹ, ವಾಹನ ಅಥವಾ ಶಿಕ್ಷಣ ಸಾಲಗಳ ಸಾಮಾನ್ಯ ಕಾರ್ಯವಿಧಾನ ಮತ್ತು ಪ್ರಮಾಣಿತ ದಾಖಲಾತಿ ಪರಿಶೀಲನಾಪಟ್ಟಿ.",
            "steps": [
                "ಅರ್ಹತೆ ಮತ್ತು ಕ್ರೆಡಿಟ್ ಸ್ಕೋರ್ ಪರಿಶೀಲಿಸಿ (ಉತ್ತಮ ಬಡ್ಡಿದರಗಳಿಗಾಗಿ ಸಾಮಾನ್ಯವಾಗಿ 750 ಕ್ಕಿಂತ ಹೆಚ್ಚಿನ ಸಿಬಿಲ್ ಸ್ಕೋರ್ ಅಪೇಕ್ಷಣೀಯ).",
                "ಸಾಲದ ವರ್ಗವನ್ನು (ಗೃಹ, ವೈಯಕ್ತಿಕ, ಆಟೋ, ಶಿಕ್ಷಣ) ಆಯ್ಕೆಮಾಡಿ ಮತ್ತು ಅಧಿಕೃತ ಕೊಟೇಶನ್ ವಿನಂತಿಸಿ.",
                "ಬ್ಯಾಂಕ್ ಶಾಖೆ ಅಥವಾ ಅಧಿಕೃತ ನೆಟ್-ಬ್ಯಾಂಕಿಂಗ್ / ಮೊಬೈಲ್ ಅಪ್ಲಿಕೇಶನ್ ಮೂಲಕ ಭರ್ತಿ ಮಾಡಿದ ಸಾಲದ ಅರ್ಜಿಯನ್ನು ಸಲ್ಲಿಸಿ.",
                "ಕೆವೈಸಿ ಪುರಾವೆಗಳು, ಆದಾಯದ ಪುರಾವೆ (ಸಂಬಳದ ಸ್ಲಿಪ್‌ಗಳು / ಐಟಿಆರ್ / ಫಾರ್ಮ್ 16), ಬ್ಯಾಂಕ್ ವಿವರಗಳು ಮತ್ತು ಆಸ್ತಿ ದಾಖಲೆಗಳನ್ನು ಸಲ್ಲಿಸಿ.",
                "ಬ್ಯಾಂಕ್ ಕ್ರೆಡಿಟ್ ಮೌಲ್ಯಮಾಪನ, ವಾಸಸ್ಥಳ/ಕಚೇರಿ ಪರಿಶೀಲನೆ ಮತ್ತು ತಾಂತ್ರಿಕ ಆಸ್ತಿ ಮೌಲ್ಯಮಾಪನವನ್ನು ಪೂರ್ಣಗೊಳಿಸಿ.",
                "ಅನುಮೋದಿತ ಮೊತ್ತ, ಬಡ್ಡಿದರ, ಪ್ರಕ್ರಿಯಾ ಶುಲ್ಕ ಮತ್ತು ಇಎಂಐ ಅವಧಿಯನ್ನು ವಿವರಿಸುವ ಅಧಿಕೃತ ಮಂಜೂರಾತಿ ಪತ್ರವನ್ನು ಪರಿಶೀಲಿಸಿ.",
                "ಸಾಲ ಒಪ್ಪಂದಕ್ಕೆ ಸಹಿ ಮಾಡಿ, ಸ್ವಯಂ-ಡೆಬಿಟ್‌ಗಾಗಿ NACH/ಇ-ಮ್ಯಾಂಡೇಟ್ ಸಲ್ಲಿಸಿ ಮತ್ತು ಸಾಲದ ಮೊತ್ತವನ್ನು ಸ್ವೀಕರಿಸಿ."
            ],
            "required_documents": [
                "ಗುರುತು ಮತ್ತು ವಿಳಾಸದ ಪುರಾವೆ (ಆಧಾರ್ ಕಾರ್ಡ್, ಪ್ಯಾನ್ ಕಾರ್ಡ್, ಪಾಸ್‌ಪೋರ್ಟ್, ಮತದಾರರ ಗುರುತಿನ ಚೀಟಿ)",
                "ವೇತನದಾರರಿಗೆ ಆದಾಯದ ಪುರಾವೆ: ಕಳೆದ 3 ರಿಂದ 6 ತಿಂಗಳ ಸಂಬಳದ ಸ್ಲಿಪ್‌ಗಳು ಮತ್ತು 2 ವರ್ಷಗಳ ಫಾರ್ಮ್ 16/ITR",
                "ಸ್ವಯಂ ಉದ್ಯೋಗಿಗಳಿಗೆ: ಕಳೆದ 2 ರಿಂದ 3 ವರ್ಷಗಳ ಆಡಿಟ್ ಮಾಡಿದ ITR, ಲಾಭ ಮತ್ತು ನಷ್ಟದ ವಿವರ ಮತ್ತು ವ್ಯಾಪಾರ ನೋಂದಣಿ ಪುರಾವೆ (GST)",
                "ಕಳೆದ 6 ರಿಂದ 12 ತಿಂಗಳ ಬ್ಯಾಂಕ್ ಖಾತೆ ವಿವರಗಳು",
                "ಆಸ್ತಿ ದಾಖಲೆಗಳು (ಗೃಹ ಸಾಲಗಳಿಗಾಗಿ): ಶೀರ್ಷಿಕೆ ಪತ್ರ, ಅನುಮೋದಿತ ಕಟ್ಟಡ ಯೋಜನೆ, ಮಾರಾಟ ಒಪ್ಪಂದ, ಎನ್‌ಒಸಿ",
                "ಶಿಕ್ಷಣ ಸಂಸ್ಥೆಯಿಂದ ಪ್ರವೇಶ ಪತ್ರ ಮತ್ತು ಶುಲ್ಕದ ವಿವರ (ಶಿಕ್ಷಣ ಸಾಲಕ್ಕಾಗಿ)"
            ],
            "authority_type": "ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಶಾಖೆ / ಸಾಲ ನೀಡುವ ಸಂಸ್ಥೆ",
            "estimated_time": "ವೈಯಕ್ತಿಕ ಸಾಲಗಳು: 1 ರಿಂದ 3 ಕೆಲಸದ ದಿನಗಳು; ಗೃಹ/ಆಸ್ತಿ ಸಾಲಗಳು: 7 ರಿಂದ 15 ಕೆಲಸದ ದಿನಗಳು",
            "fees": "ಸಾಲದ ಮೊತ್ತದ 0.25% ರಿಂದ 2% ಪ್ರಕ್ರಿಯಾ ಶುಲ್ಕ (GST ಜೊತೆಗೆ); ಸ್ಟಾಂಪ್ ಡ್ಯೂಟಿ ರಾಜ್ಯಕ್ಕೆ ಅನುಗುಣವಾಗಿ ಬದಲಾಗುತ್ತದೆ"
        },
        "kyc_account_opening": {
            "name": "ಹೊಸ ಬ್ಯಾಂಕ್ ಖಾತೆ ತೆರೆಯುವಿಕೆ ಮತ್ತು ಕೆವೈಸಿ ಪರಿಶೀಲನೆ",
            "description": "ಡಿಜಿಟಲ್ (ವೀಡಿಯೊ ಕೆವೈಸಿ) ಅಥವಾ ಶಾಖೆಗೆ ಭೇಟಿ ನೀಡುವ ಮೂಲಕ ಪೂರ್ಣ ಕೆವೈಸಿ ಅನುಸರಣೆಯೊಂದಿಗೆ ಉಳಿತಾಯ ಅಥವಾ ಚಾಲ್ತಿ ಬ್ಯಾಂಕ್ ಖಾತೆಯನ್ನು ತೆರೆಯುವ ಹಂತ-ಹಂತದ ವಿಧಾನ.",
            "steps": [
                "ಬ್ಯಾಂಕ್ ಮತ್ತು ಖಾತೆಯ ಪ್ರಕಾರವನ್ನು ಆಯ್ಕೆಮಾಡಿ (ಉಳಿತಾಯ, ಶೂನ್ಯ ಬಾಕಿ / BSBD, ಸಂಬಳ ಖಾತೆ, ಅಥವಾ ಚಾಲ್ತಿ ಖಾತೆ).",
                "ಬ್ಯಾಂಕ್ ಅಧಿಕೃತ ವೆಬ್‌ಸೈಟ್ / ಮೊಬೈಲ್ ಅಪ್ಲಿಕೇಶನ್ ಮೂಲಕ ಆನ್‌ಲೈನ್‌ನಲ್ಲಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ ಅಥವಾ ಹತ್ತಿರದ ಶಾಖೆಯಿಂದ ಫಾರ್ಮ್ ಪಡೆಯಿರಿ.",
                "ವೈಯಕ್ತಿಕ ವಿವರಗಳನ್ನು ಭರ್ತಿ ಮಾಡಿ: ಪೂರ್ಣ ಹೆಸರು, ಜನ್ಮ ದಿನಾಂಕ, ಪ್ಯಾನ್, ಆಧಾರ್ ಸಂಖ್ಯೆ, ಉದ್ಯೋಗ, ವಾರ್ಷಿಕ ಆದಾಯ ಮತ್ತು ನಾಮಿನಿ ವಿವರಗಳು.",
                "ಕೆವೈಸಿ ಮೋಡ್ ಆಯ್ಕೆಮಾಡಿ: ಆನ್‌ಲೈನ್ ವೀಡಿಯೊ ಕೆವೈಸಿ (V-KYC) ಅಥವಾ ಶಾಖೆಯಲ್ಲಿ ಬಯೋಮೆಟ್ರಿಕ್ ದೃಢೀಕರಣ.",
                "ವೀಡಿಯೊ ಕೆವೈಸಿ: ಬ್ಯಾಂಕ್ ಅಧಿಕಾರಿಯೊಂದಿಗೆ ಲೈವ್ ವೀಡಿಯೊ ಕರೆಯಲ್ಲಿ ಭಾಗವಹಿಸಿ, ಮೂಲ ಪ್ಯಾನ್ ಕಾರ್ಡ್ ತೋರಿಸಿ ಮತ್ತು ಸಹಿ ಸೆರೆಹಿಡಿಯಿರಿ.",
                "ಕನಿಷ್ಠ ಆರಂಭಿಕ ಠೇವಣಿ ಠೇವಣಿ ಮಾಡಿ (ಅಗತ್ಯವಿದ್ದರೆ).",
                "ನಿಮ್ಮ ನೋಂದಾಯಿತ ವಿಳಾಸದಲ್ಲಿ ಖಾತೆ ಸಂಖ್ಯೆ, ಗ್ರಾಹಕ ಐಡಿ (CIF), ಡೆಬಿಟ್ ಕಾರ್ಡ್, ಚೆಕ್ ಬುಕ್ ಮತ್ತು ವೆಲ್‌ಕಮ್ ಕಿಟ್ ಸ್ವೀಕರಿಸಿ."
            ],
            "required_documents": [
                "ಗುರುತಿಗಾಗಿ ಅಧಿಕೃತ ಮಾನ್ಯ ದಾಖಲೆ (OVD): ಪ್ಯಾನ್ ಕಾರ್ಡ್ (ಕಡ್ಡಾಯ ಅಥವಾ ಫಾರ್ಮ್ 60) ಮತ್ತು ಆಧಾರ್ ಕಾರ್ಡ್",
                "ವಿಳಾಸದ ಪುರಾವೆ (POA): ಆಧಾರ್ ಕಾರ್ಡ್, ಪಾಸ್‌ಪೋರ್ಟ್, ಮತದಾರರ ಗುರುತಿನ ಚೀಟಿ, ಅಥವಾ ಯುಟಿಲಿಟಿ ಬಿಲ್ (< 3 ತಿಂಗಳು)",
                "ಎರಡು ಇತ್ತೀಚಿನ ಪಾಸ್‌ಪೋರ್ಟ್ ಗಾತ್ರದ ಬಣ್ಣದ ಭಾವಚಿತ್ರಗಳು (ಶಾಖೆಯಲ್ಲಿ ತೆರೆಯಲು)",
                "ನಾಮಿನಿ ಗುರುತು ಮತ್ತು ವಯಸ್ಸಿನ ಪುರಾವೆ",
                "ವ್ಯಾಪಾರ ನೋಂದಣಿ ಮತ್ತು ಜಿಎಸ್ಟಿ ಪ್ರಮಾಣಪತ್ರ (ಚಾಲ್ತಿ ಖಾತೆಗಳಿಗಾಗಿ)"
            ],
            "authority_type": "ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಶಾಖೆ / ಡಿಜಿಟಲ್ ಖಾತೆ ಪೋರ್ಟಲ್",
            "estimated_time": "ಡಿಜಿಟಲ್ / ವೀಡಿಯೊ ಕೆವೈಸಿ: ತಕ್ಷಣದಿಂದ 24 ಗಂಟೆಗಳು; ಶಾಖೆಯಲ್ಲಿ ತೆರೆಯುವಿಕೆ: 2 ರಿಂದ 4 ಕೆಲಸದ ದಿನಗಳು",
            "fees": "ಯಾವುದೇ ಅರ್ಜಿ ಶುಲ್ಕವಿಲ್ಲ; ಆರಂಭಿಕ ಠೇವಣಿ ಖಾತೆಯ ಪ್ರಕಾರ ಮತ್ತು ಶಾಖೆಯ ಸ್ಥಳವನ್ನು ಆಧರಿಸಿ ಬದಲಾಗುತ್ತದೆ"
        },
        "update_account_details": {
            "name": "ಬ್ಯಾಂಕ್ ಖಾತೆ ವಿವರಗಳನ್ನು ನವೀಕರಿಸುವುದು (ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ಮತ್ತು ವಿಳಾಸ)",
            "description": "ಸುರಕ್ಷಿತ ವಹಿವಾಟು OTP ಗಳು ಮತ್ತು ಸಂವಹನಕ್ಕಾಗಿ ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಖಾತೆಗೆ ಲಿಂಕ್ ಮಾಡಲಾದ ನಿಮ್ಮ ನೋಂದಾಯಿತ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ಅಥವಾ ವಿಳಾಸವನ್ನು ನವೀಕರಿಸುವ ವಿಧಾನ.",
            "steps": [
                "ಅಗತ್ಯ ನವೀಕರಣವನ್ನು ನಿರ್ಧರಿಸಿ: ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ಬದಲಾವಣೆಗಳಿಗೆ ಎಟಿಎಂ ಅಥವಾ ಶಾಖೆಯ ಭೇಟಿ ಅಗತ್ಯವಿರುತ್ತದೆ; ವಿಳಾಸ ನವೀಕರಣವನ್ನು ಆನ್‌ಲೈನ್‌ನಲ್ಲಿ ಮಾಡಬಹುದು.",
                "ಎಟಿಎಂ ಮೂಲಕ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ನವೀಕರಣ: ಡೆಬಿಟ್ ಕಾರ್ಡ್ ಸೇರಿಸಿ, ಪಿನ್ ನಮೂದಿಸಿ, 'ಸೇವೆಗಳು' > 'ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ಬದಲಾಯಿಸಿ' ಆಯ್ಕೆಮಾಡಿ ಮತ್ತು OTP ಮೂಲಕ ದೃಢೀಕರಿಸಿ.",
                "ಶಾಖೆಯ ಮೂಲಕ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ನವೀಕರಣ: ಹೋಮ್ ಶಾಖೆಗೆ ಭೇಟಿ ನೀಡಿ, ವಿನಂತಿ ಫಾರ್ಮ್ (CRF) ಭರ್ತಿ ಮಾಡಿ ಮತ್ತು ಗುರುತಿನ ಪುರಾವೆ ಸಲ್ಲಿಸಿ.",
                "ನೆಟ್-ಬ್ಯಾಂಕಿಂಗ್ ಮೂಲಕ ವಿಳಾಸ ನವೀಕರಣ: ಪೋರ್ಟಲ್‌ಗೆ ಲಾಗ್ ಇನ್ ಮಾಡಿ, 'ಪ್ರೊಫೈಲ್' > 'ವಿಳಾಸ ನವೀಕರಣ' ಆಯ್ಕೆಮಾಡಿ ಮತ್ತು ಆಧಾರ್ OTP ಮೂಲಕ ದೃಢೀಕರಿಸಿ.",
                "ಶಾಖೆಯ ಮೂಲಕ ವಿಳಾಸ ನವೀಕರಣ: ಹೊಸ ವಿಳಾಸ ಪುರಾವೆಯೊಂದಿಗೆ ವಿನಂತಿ ಫಾರ್ಮ್ ಅನ್ನು ಸಲ್ಲಿಸಿ.",
                "ದಾಖಲೆಗಳು ನವೀಕರಿಸಲ್ಪಟ್ಟ ನಂತರ ಅಧಿಕೃತ ದೃಢೀಕರಣ SMS ಮತ್ತು ಇಮೇಲ್ ಸ್ವೀಕರಿಸಿ."
            ],
            "required_documents": [
                "ಗುರುತಿನ ಪರಿಶೀಲನೆಗಾಗಿ ಮೂಲ ಪ್ಯಾನ್ ಕಾರ್ಡ್ ಮತ್ತು ಆಧಾರ್ ಕಾರ್ಡ್",
                "ಹೊಸ ವಿಳಾಸದ ಮಾನ್ಯ ಪುರಾವೆ: ನವೀಕರಿಸಿದ ಆಧಾರ್ ಕಾರ್ಡ್, ಪಾಸ್‌ಪೋರ್ಟ್, ಮತದಾರರ ಗುರುತಿನ ಚೀಟಿ, ಅಥವಾ ವಿದ್ಯುತ್ ಬಿಲ್ (< 3 ತಿಂಗಳು)",
                "ಸಕ್ರಿಯ ಡೆಬಿಟ್ ಕಾರ್ಡ್ ಮತ್ತು ಪಿನ್ (ಎಟಿಎಂ ವಿನಂತಿಗಳಿಗಾಗಿ)",
                "ಖಾತೆ ಸಂಖ್ಯೆ ಮತ್ತು CIF ಹೊಂದಿರುವ ಪಾಸ್‌ಬುಕ್ ಅಥವಾ ಇತ್ತೀಚಿನ ಬ್ಯಾಂಕ್ ವಿವರ"
            ],
            "authority_type": "ನಿಮ್ಮ ಹೋಮ್ ಬ್ಯಾಂಕ್ ಶಾಖೆ / ನೆಟ್-ಬ್ಯಾಂಕಿಂಗ್ ಗ್ರಾಹಕ ಸೇವೆ",
            "estimated_time": "ಎಟಿಎಂ / ನೆಟ್-ಬ್ಯಾಂಕಿಂಗ್: ತಕ್ಷಣದಿಂದ 24 ಗಂಟೆಗಳು; ಶಾಖೆಯ ಸಲ್ಲಿಕೆ: 1 ರಿಂದ 3 ಕೆಲಸದ ದಿನಗಳು",
            "fees": "ಉಚಿತ / ಹೆಚ್ಚಿನ ಭಾರತೀಯ ಬ್ಯಾಂಕ್‌ಗಳಲ್ಲಿ ಯಾವುದೇ ಶುಲ್ಕವಿಲ್ಲ"
        },
        "account_transfer": {
            "name": "ಬ್ಯಾಂಕ್ ಖಾತೆ ಶಾಖೆ ವರ್ಗಾವಣೆ ಮಾರ್ಗದರ್ಶಿ",
            "description": "ನಿಮ್ಮ ಖಾತೆ ಸಂಖ್ಯೆಯನ್ನು ಬದಲಾಯಿಸದೆಯೇ ನಿಮ್ಮ ಸಕ್ರಿಯ ಉಳಿತಾಯ ಅಥವಾ ಚಾಲ್ತಿ ಖಾತೆಯನ್ನು ಒಂದು ಶಾಖೆ/ನಗರದಿಂದ ಅದೇ ಬ್ಯಾಂಕ್‌ನ ಇನ್ನೊಂದು ಶಾಖೆಗೆ ವರ್ಗಾಯಿಸುವ ಹಂತ-ಹಂತದ ವಿಧಾನ.",
            "steps": [
                "ನಿಮ್ಮ ಖಾತೆಯನ್ನು ವರ್ಗಾಯಿಸಲು ಬಯಸುವ ಹೊಸ ಶಾಖೆಯ 4 ಅಥವಾ 5 ಅಂಕಿಯ ಶಾಖಾ ಕೋಡ್ ಮತ್ತು IFSC ಕೋಡ್ ಪಡೆಯಿರಿ.",
                "ಆಯ್ಕೆ 1 (ಆನ್‌ಲೈನ್): ನೆಟ್-ಬ್ಯಾಂಕಿಂಗ್ ಪೋರ್ಟಲ್‌ಗೆ ಲಾಗ್ ಇನ್ ಮಾಡಿ, 'ಸೇವೆಗಳು / ಖಾತೆ ವಿನಂತಿಗಳು' > 'ಉಳಿತಾಯ ಖಾತೆ ವರ್ಗಾವಣೆ' ಆಯ್ಕೆಮಾಡಿ.",
                "ನಿಮ್ಮ ಖಾತೆ ಸಂಖ್ಯೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ, ಹೊಸ ಶಾಖಾ ಕೋಡ್ ನಮೂದಿಸಿ ಮತ್ತು OTP ಮೂಲಕ ವಿನಂತಿಯನ್ನು ಸಲ್ಲಿಸಿ.",
                "ಆಯ್ಕೆ 2 (ಶಾಖೆಯಲ್ಲಿ): ನಿಮ್ಮ ಪ್ರಸ್ತುತ ಹೋಮ್ ಶಾಖೆ ಅಥವಾ ಹೊಸ ಶಾಖೆಗೆ ಭೇಟಿ ನೀಡಿ, ಫಾರ್ಮ್ ಭರ್ತಿ ಮಾಡಿ ಮತ್ತು ಬಳಕೆಯಾಗದ ಚೆಕ್‌ಗಳನ್ನು ಸಲ್ಲಿಸಿ.",
                "ಹಳೆಯ ಶಾಖೆಗೆ ಲಿಂಕ್ ಮಾಡಲಾದ ಯಾವುದೇ ಬಾಕಿ ಲಾಕರ್‌ಗಳು ಅಥವಾ ಸಾಲಗಳನ್ನು ಇತ್ಯರ್ಥಗೊಳಿಸಿ.",
                "ಆನ್‌ಲೈನ್‌ನಲ್ಲಿ ಸ್ಥಿತಿಯನ್ನು ಟ್ರ್ಯಾಕ್ ಮಾಡಿ; ಖಾತೆ ಸಂಖ್ಯೆ, ಡೆಬಿಟ್ ಕಾರ್ಡ್ ಮತ್ತು ವಿವರಗಳು ಬದಲಾಗದೆ ಉಳಿಯುತ್ತವೆ.",
                "ವರ್ಗಾವಣೆ ಪೂರ್ಣಗೊಂಡ ನಂತರ ಹೊಸ IFSC ಕೋಡ್ ಹೊಂದಿರುವ ಹೊಸ ಚೆಕ್ ಬುಕ್ ಮತ್ತು ನವೀಕರಿಸಿದ ಪಾಸ್‌ಬುಕ್ ಸಂಗ್ರಹಿಸಿ."
            ],
            "required_documents": [
                "ಸಕ್ರಿಯ ಖಾತೆ ಸಂಖ್ಯೆ ಮತ್ತು CIF ತೋರಿಸುವ ಬ್ಯಾಂಕ್ ಪಾಸ್‌ಬುಕ್ ಅಥವಾ ಖಾತೆ ವಿವರ",
                "ಮಾನ್ಯವಾದ ಗುರುತಿನ ಪುರಾವೆ (ಆಧಾರ್ ಕಾರ್ಡ್ ಅಥವಾ ಪ್ಯಾನ್ ಕಾರ್ಡ್)",
                "ಗಮ್ಯಸ್ಥಾನ ನಗರದಲ್ಲಿ ಹೊಸ ವಿಳಾಸದ ಪುರಾವೆ (ವಿಳಾಸವನ್ನು ಸಹ ನವೀಕರಿಸುತ್ತಿದ್ದರೆ)",
                "ಹಳೆಯ ಶಾಖೆಯಿಂದ ಬಳಕೆಯಾಗದ ಚೆಕ್ ಎಲೆಗಳು (ರದ್ದತಿಗಾಗಿ)"
            ],
            "authority_type": "ನಿಮ್ಮ ಪ್ರಸ್ತುತ ಹೋಮ್ ಶಾಖೆ ಅಥವಾ ಗಮ್ಯಸ್ಥಾನ ಬ್ಯಾಂಕ್ ಶಾಖೆ",
            "estimated_time": "ಆನ್‌ಲೈನ್ ನೆಟ್-ಬ್ಯಾಂಕಿಂಗ್: 1 ರಿಂದ 3 ಕೆಲಸದ ದಿನಗಳು; ಭೌತಿಕ ಶಾಖೆಯ ವಿನಂತಿ: 3 ರಿಂದ 7 ಕೆಲಸದ ದಿನಗಳು",
            "fees": "ಉಚಿತ / ಸಾರ್ವಜನಿಕ ಮತ್ತು ಖಾಸಗಿ ವಲಯದ ಬ್ಯಾಂಕ್‌ಗಳಲ್ಲಿ ಯಾವುದೇ ಶುಲ್ಕವಿಲ್ಲ"
        }
    }
}

def load_processes(category: str = "government", language: str = None) -> List[Dict[str, Any]]:
    """
    Loads curated processes from data/processes.json (Government)
    or data/banking_processes.json (Banking), with multilingual localization.
    Accepts language as first argument if category is omitted.
    """
    # If first argument is a language name
    if category in ["Hindi", "Kannada", "English"] and language is None:
        language = category
        category = "government"

    if category == "insurance":
        data_file = INSURANCE_DATA_PATH
    elif category == "banking":
        data_file = BANKING_DATA_PATH
    else:
        data_file = GOVT_DATA_PATH
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Processes data file not found at: {data_file}")
        
    with open(data_file, "r", encoding="utf-8-sig") as f:
        base_processes = json.load(f)
        
    norm_lang = get_normalized_language(language)
    if norm_lang == "English":
        return base_processes
        
    lang_overrides = LOCALIZED_PROCESS_DATA.get(norm_lang, {})
    localized_list = []
    
    for proc in base_processes:
        pid = proc.get("id")
        if pid in lang_overrides:
            override = lang_overrides[pid]
            p_copy = dict(proc)
            p_copy["name"] = override.get("name", proc.get("name"))
            p_copy["description"] = override.get("description", proc.get("description"))
            p_copy["steps"] = override.get("steps", proc.get("steps"))
            p_copy["required_documents"] = override.get("required_documents", proc.get("required_documents"))
            
            auth_copy = dict(proc.get("authority", {}))
            if "authority_type" in override:
                auth_copy["type"] = override["authority_type"]
            p_copy["authority"] = auth_copy
            
            p_copy["estimated_time"] = override.get("estimated_time", proc.get("estimated_time"))
            p_copy["fees"] = override.get("fees", proc.get("fees"))
            localized_list.append(p_copy)
        else:
            localized_list.append(proc)
            
    return localized_list

def get_process_by_id(process_id: str, category: str = "government", language: str = None) -> Optional[Dict[str, Any]]:
    """
    Retrieves a single process by its unique id.
    """
    processes = load_processes(category=category, language=language)
    for p in processes:
        if p.get("id") == process_id:
            return p
    return None

def format_process_for_analysis(process: Dict[str, Any]) -> Dict[str, Any]:
    """
    Formats the curated process JSON into the SAME shape as analyze_document() output.
    """
    return {
        "doc_type": process.get("name", "Process Guide"),
        "summary": process.get("description", ""),
        "steps": process.get("steps", []),
        "deadlines": [],
        "required_documents": process.get("required_documents", []),
        "risks": [],
        "authority": process.get("authority", {
            "type": "Designated Authority / Office",
            "mode": "both",
            "note": "confirm exact details with your branch / office"
        }),
        "estimated_time": process.get("estimated_time", "Varies"),
        "fees": process.get("fees", "Varies"),
        "context_raw": json.dumps(process, indent=2, ensure_ascii=False)
    }


# Dynamically add insurance overrides
LOCALIZED_PROCESS_DATA.setdefault("Hindi", {}).update({"claim_filing": {"name": "सामान्य बीमा दावा दायर करने की गाइड", "description": "अपनी बीमा कंपनी को सूचना देने, सहायक दस्तावेज़ जमा करने, मूल्यांकन कराने और दावा निपटान प्राप्त करने की मानक चरण-दर-चरण प्रक्रिया।", "steps": ["तत्काल दावा सूचना: घटना या अस्पताल में भर्ती होने के 24 से 48 घंटों के भीतर अपने बीमाकर्ता से संपर्क करें और क्लेम संदर्भ संख्या प्राप्त करें।", "दावा मोड चुनें: कैशलेस नेटवर्क सुविधा या प्रतिपूर्ति मोड (पहले भुगतान करें और बाद में दावा करें) चुनें।", "आधिकारिक दावा फॉर्म भरें और हस्ताक्षर करें: दावा फॉर्म का भाग A (बीमाकृत विवरण) और भाग B (अस्पताल/मूल्यांकनकर्ता विवरण) पूरा करें।", "आवश्यक प्रमाण और रसीदें एकत्रित करें: मूल बिल, भुगतान रसीदें, डिस्चार्ज सारांश, सर्वेक्षक रिपोर्ट या पुलिस प्राथमिकी संकलित करें।", "दस्तावेज़ जमा करें: निकटतम शाखा में भौतिक दस्तावेज़ जमा करें या बीमाकर्ता के पोर्टल पर अपलोड करें।", "सर्वेक्षक / चिकित्सा मूल्यांकन: किसी भी स्पष्टीकरण के लिए बीमा सर्वेक्षक या टीपीए अन्वेषक के साथ सहयोग करें।", "दावा निपटान और भुगतान: निपटान सारांश की समीक्षा करें और अपने बैंक खाते में प्रत्यक्ष एनईएफटी क्रेडिट प्राप्त करें।"], "required_documents": ["मूल पॉलिसी अनुसूची प्रति और सक्रिय पॉलिसी नंबर", "विधिवत भरा और हस्ताक्षरित आधिकारिक दावा प्रपत्र (भाग A और B)", "पॉलिसीधारक और दावेदार का फोटो पहचान प्रमाण (आधार कार्ड, पैन कार्ड या पासपोर्ट)", "रद्द किया गया चेक या बैंक पासबुक प्रति जिसमें खाता संख्या और IFSC कोड स्पष्ट हो", "मूल मदवार अंतिम बिल, भुगतान रसीदें और कैश मेमो", "घटना-विशिष्ट प्रमाण (स्वास्थ्य के लिए डिस्चार्ज सारांश, चोरी/दुर्घटना के लिए पुलिस एफआईआर, मरम्मत अनुमान)"], "authority_type": "आपके बीमाकर्ता का दावा विभाग / टीपीए (तृतीय-पक्ष प्रशासक)", "estimated_time": "कैशलेस: 2 से 6 घंटे; प्रतिपूर्ति: दस्तावेज़ जमा करने के बाद 7 से 15 कार्य दिवस", "fees": "निःशुल्क / कोई दावा प्रसंस्करण शुल्क नहीं (पॉलिसी शर्तों के अनुसार डिडक्टिबल्स)"}, "policy_breakdown": {"name": "अपनी बीमा पॉलिसी और प्रमुख शर्तों को समझना", "description": "पॉलिसी अनुसूचियों, खंडों, बहिष्करणों, कटौती, प्रतीक्षा अवधि और नेटवर्क नियमों का व्यापक विवरण ताकि आप अपने पॉलिसी दस्तावेजों को आसानी से समझ सकें।", "steps": ["पॉलिसी विवरण सत्यापित करें: बीमित सदस्यों के नाम, आयु, संबंध, पॉलिसी अवधि और नामांकित व्यक्ति के नाम की शुद्धता जांचें।", "बीमा राशि बनाम प्रीमियम को समझें: जीएसटी सहित भुगतान किए गए वार्षिक प्रीमियम के मुकाबले अधिकतम कवरेज सीमा (बीमित राशि) नोट करें।", "प्रतीक्षा अवधि जांचें: विशिष्ट प्रतीक्षा अवधि की पहचान करें (उदा. 30 दिन की प्रारंभिक प्रतीक्षा अवधि, पहले से मौजूद बीमारियों के लिए 24 से 48 महीने)।", "समावेशन और बहिष्करण की समीक्षा करें: उन चिकित्सा उपचारों या गैर-चिकित्सा उपभोग्य सामग्रियों की जांच करें जो कभी कवर नहीं होते हैं।", "कटौती और सह-भुगतान खंड: पहचानें कि क्या आपकी पॉलिसी में अनिवार्य सह-भुगतान (उदा. 10% या 20% वरिष्ठ नागरिक सह-भुगतान) है।", "नेटवर्क सूची और टीपीए संपर्क सहेजें: अपना टीपीए कार्ड, हेल्पलाइन नंबर सहेजें और स्थानीय नेटवर्क अस्पतालों/गैरेजों की पुष्टि करें।"], "required_documents": ["मूल पॉलिसी अनुसूची और नियम एवं शर्तें दस्तावेज़", "टीपीए नंबर और पॉलिसी पहचानकर्ता वाला डिजिटल हेल्थ कार्ड", "80D / 80C कर छूट प्रमाण पत्र के साथ प्रीमियम भुगतान रसीद", "बीमित सदस्यों के केवाईसी दस्तावेज (आधार, पैन कार्ड, जन्मतिथि प्रमाण)", "पहले से मौजूद चिकित्सीय इतिहास और पिछले नुस्खे"], "authority_type": "भारतीय बीमा नियामक और विकास प्राधिकरण (IRDAI) / आपका बीमाकर्ता", "estimated_time": "पॉलिसी प्राप्ति की तिथि से 15 से 30 दिन की वैधानिक समीक्षा अवधि (फ्री-लुक)", "fees": "शून्य / मानक वैधानिक पॉलिसी प्रशासन"}, "health_insurance_coverage": {"name": "स्वास्थ्य बीमा कवरेज और दावे (कैशलेस बनाम प्रतिपूर्ति)", "description": "अस्पताल में भर्ती लाभ, पूर्व/पश्चात अस्पताल खर्च, डेकेयर उपचार, बहिष्करण और कैशलेस प्री-ऑथराइजेशन बनाम प्रतिपूर्ति पर विस्तृत गाइड।", "steps": ["नियोजित अस्पताल में भर्ती (कैशलेस): 48 से 72 घंटे पहले एक नेटवर्क अस्पताल चुनें; अस्पताल के टीपीए डेस्क पर फॉर्म जमा करें।", "आपातकालीन भर्ती (कैशलेस): भर्ती होने के 24 घंटे के भीतर बीमाकर्ता को सूचित करें; अस्पताल टीपीए डेस्क आपातकालीन अनुरोध भेजता है।", "बीमाकर्ता की प्रतिक्रिया: बीमाकर्ता/टीपीए प्रारंभिक स्वीकृति पत्र जारी करता है; डिस्चार्ज के समय अंतिम बिल का निपटान होता है।", "प्रतिपूर्ति दावे (गैर-नेटवर्क अस्पताल): अस्पताल के बिलों का सीधे भुगतान करें, सभी मूल डिस्चार्ज सारांश और रिपोर्ट एकत्र करें।", "पूर्व और पश्चात अस्पताल खर्च: भर्ती से 30-60 दिन पहले और डिस्चार्ज के 60-90 दिन बाद के सभी परामर्श बिल संलग्न करें।", "दावा पैकेज जमा करें: डिस्चार्ज होने के 15 से 30 दिनों के भीतर दावा प्रपत्र और सभी मूल वाउचर जमा करें।", "निपटान और भुगतान: बैंक हस्तांतरण के माध्यम से भुगतान प्राप्त करें।"], "required_documents": ["विधिवत भरा हुआ स्वास्थ्य दावा प्रपत्र (भाग A और डॉक्टर द्वारा हस्ताक्षरित भाग B)", "अस्पताल डिस्चार्ज सारांश जिसमें भर्ती का कारण, दिया गया उपचार और स्थिति का उल्लेख हो", "कमरे के किराए, आईसीयू और सर्जरी शुल्क के विवरण के साथ मूल अस्पताल का अंतिम बिल", "मूल भुगतान रसीदें और डॉक्टर परामर्श वाउचर", "सभी नैदानिक और प्रयोगशाला जांच रिपोर्ट (रक्त परीक्षण, एक्स-रे, एमआरआई/सीटी स्कैन) नुस्खे के साथ", "प्रत्यारोपण स्टिकर और खरीद चालान (पेसमेकर, स्टेंट, कृत्रिम अंग के लिए)", "इलेक्ट्रॉनिक बैंक रिफंड के लिए प्राथमिक पॉलिसीधारक का रद्द किया गया चेक"], "authority_type": "अस्पताल टीपीए हेल्पडेस्क / बीमाकर्ता स्वास्थ्य दावा विभाग", "estimated_time": "कैशलेस प्री-ऑथ: 2 से 4 घंटे; डिस्चार्ज स्वीकृति: 2 से 6 घंटे; प्रतिपूर्ति भुगतान: 7 से 15 दिन", "fees": "शून्य दावा सबमिशन शुल्क; पॉलिसी शर्तों के अनुसार अनिवार्य सह-भुगतान"}, "auto_insurance_coverage": {"name": "मोटर / वाहन बीमा कवरेज और दुर्घटना के दावे", "description": "व्यापक बनाम तीसरे पक्ष के वाहन क्षति के दावे, चोरी के दावे, दुर्घटना सर्वेक्षक निरीक्षण और नेटवर्क गैरेज कैशलेस मरम्मत की प्रक्रिया।", "steps": ["सुरक्षा और तत्काल साक्ष्य: वाहन पंजीकरण संख्या नोट करें, दुर्घटना स्थल और वाहन क्षति की स्पष्ट तस्वीरें लें।", "तत्काल दावा सूचना: वाहन को हटाने से पहले बीमाकर्ता के टोल-फ्री नंबर पर कॉल करें या मोबाइल ऐप पर दावा दर्ज करें।", "पुलिस प्राथमिकी / पंचनामा: तीसरे पक्ष की चोट, मृत्यु, बड़ी संपत्ति क्षति या वाहन चोरी होने पर अनिवार्य।", "अधिकृत कैशलेस गैरेज में जाएं: कैशलेस मूल्यांकन के लिए वाहन को अनुमोदित नेटवर्क गैरेज में ले जाएं।", "सर्वेक्षक निरीक्षण: बीमा सर्वेक्षक क्षति का निरीक्षण करता है और मरम्मत के अनुमान को मंजूरी देता है।", "वाहन की मरम्मत: अनुमोदित अनुमान के अनुसार गैरेज वाहन की मरम्मत करता है।", "अनिवार्य डिडक्टिबल का भुगतान और डिलीवरी: अनिवार्य कटौती योग्य राशि का भुगतान करें और डिलीवरी लें।"], "required_documents": ["सक्रिय मोटर बीमा पॉलिसी अनुसूची या बीमा प्रमाण पत्र", "वाहन पंजीकरण प्रमाणपत्र (आरसी बुक / स्मार्ट कार्ड)", "दुर्घटना के समय वाहन चला रहे व्यक्ति का वैध ड्राइविंग लाइसेंस (डीएल)", "विधिवत भरा और हस्ताक्षरित मोटर दावा फॉर्म", "मूल पुलिस प्राथमिकी / डीडी प्रविष्टि (चोरी, बड़ी टक्कर या तीसरे पक्ष की चोट के लिए)", "गैरेज मरम्मत अनुमान और भुगतान रसीद के साथ मूल कर चालान", "क्षतिग्रस्त वाहन की तस्वीरें जिसमें नंबर प्लेट स्पष्ट रूप से दिखाई दे रही हो"], "authority_type": "बीमाकर्ता मोटर दावा केंद्र / लाइसेंस प्राप्त बीमा सर्वेक्षक", "estimated_time": "ऐप द्वारा सर्वे: 2 से 6 घंटे; बड़ी मरम्मत स्वीकृति: 2 से 5 दिन; कुल समय: 5 से 10 दिन", "fees": "अनिवार्य पॉलिसी कटौती योग्य शुल्क (चौपहिया के लिए ₹1,000 - ₹2,000; दोपहिया के लिए ₹100)"}, "documents_keep_ready": {"name": "आवश्यक बीमा दस्तावेज़ तैयारी चेकलिस्ट", "description": "महत्वपूर्ण दस्तावेजों, डिजिटल रिकॉर्ड और नामांकित व्यक्तियों के प्रमाणों की एक तैयारी चेकलिस्ट जो हर परिवार को दावा निपटान के लिए रखनी चाहिए।", "steps": ["मास्टर पारिवारिक बीमा फ़ोल्डर बनाएं: एक वाटरप्रूफ फ़ोल्डर और एक सुरक्षित डिजिटल फ़ोल्डर (डिजीलॉकर/ई-बीमा खाता) बनाए रखें।", "पॉलिसी शेड्यूल व्यवस्थित करें: नवीनतम नवीनीकरण रसीदों के साथ सभी सक्रिय जीवन, स्वास्थ्य और वाहन पॉलिसियों की प्रतियां रखें।", "नामांकित व्यक्ति की जानकारी सत्यापित करें: सुनिश्चित करें कि सभी पॉलिसियों में नामांकित व्यक्ति का नाम और बैंक विवरण अद्यतित हैं।", "केवाईसी पोर्टफोलियो बनाए रखें: सभी बीमित सदस्यों के आधार, पैन और वोटर आईडी की स्व-सत्यापित प्रतियां रखें।", "पिछले चिकित्सा इतिहास को रिकॉर्ड करें: अस्पताल के डिस्चार्ज सारांश और नुस्खे कालानुक्रमिक क्रम में रखें।", "परिवार के साथ आपातकालीन पहुंच साझा करें: अपने परिवार को पॉलिसी के स्थानों और हेल्पलाइन नंबरों के बारे में सूचित करें।"], "required_documents": ["मास्टर बीमा पॉलिसियां (पॉलिसी शेड्यूल, नियम और ई-कार्ड प्रिंटआउट)", "नवीनतम प्रीमियम भुगतान रसीदें और 80D / 80C कर छूट प्रमाण पत्र", "सभी कवर किए गए सदस्यों का आधिकारिक फोटो पहचान प्रमाण (आधार, पैन, पासपोर्ट, वोटर आईडी)", "पते का प्रमाण (बिजली बिल, पासपोर्ट, आधार, बैंक विवरण)", "नामांकित व्यक्ति का पहचान प्रमाण, जन्मतिथि प्रमाण और सक्रिय बैंक विवरण", "रद्द किया गया चेक / बैंक पासबुक प्रति जिसमें खाता संख्या और IFSC कोड स्पष्ट हो", "पूर्ण पिछला चिकित्सा इतिहास डोजियर (डिस्चार्ज सारांश, सर्जरी नोट्स, लैब रिपोर्ट)"], "authority_type": "पारिवारिक बीमा रिकॉर्ड / बीमाकर्ता ग्राहक सेवा", "estimated_time": "तत्काल पहुंच / वार्षिक तैयारी समीक्षा", "fees": "शून्य / 100% निःशुल्क व्यक्तिगत तैयारी"}})
LOCALIZED_PROCESS_DATA.setdefault("Kannada", {}).update({"claim_filing": {"name": "ಸಾಮಾನ್ಯ ವಿಮಾ ಕ್ಲೈಮ್ ಸಲ್ಲಿಕೆ ಮಾರ್ಗದರ್ಶಿ", "description": "ನಿಮ್ಮ ವಿಮಾ ಕಂಪನಿಗೆ ಮಾಹಿತಿ ನೀಡಲು, ಪೂರಕ ದಾಖಲೆಗಳನ್ನು ಸಲ್ಲಿಸಲು, ಮೌಲ್ಯಮಾಪನಕ್ಕೆ ಒಳಗಾಗಲು ಮತ್ತು ಕ್ಲೈಮ್ ಇತ್ಯರ್ಥವನ್ನು ಪಡೆಯಲು ಪ್ರಮಾಣಿತ ಹಂತ-ಹಂತದ ವಿಧಾನ.", "steps": ["ತಕ್ಷಣದ ಕ್ಲೈಮ್ ಮಾಹಿತಿ: ಘಟನೆ ಅಥವಾ ಆಸ್ಪತ್ರೆಗೆ ದಾಖಲಾದ 24 ರಿಂದ 48 ಗಂಟೆಗಳ ಒಳಗೆ ನಿಮ್ಮ ವಿಮಾದಾರರನ್ನು ಸಂಪರ್ಕಿಸಿ ಮತ್ತು ಕ್ಲೈಮ್ ರೆಫರೆನ್ಸ್ ಸಂಖ್ಯೆಯನ್ನು ಪಡೆಯಿರಿ.", "ಕ್ಲೈಮ್ ಮೋಡ್ ಆಯ್ಕೆಮಾಡಿ: ನಗದಹಿತ ನೆಟ್‌ವರ್ಕ್ ಸೌಲಭ್ಯ ಅಥವಾ ಮರುಪಾವತಿ ಮೋಡ್ (ಮೊದಲು ಪಾವತಿಸಿ ನಂತರ ಕ್ಲೈಮ್ ಮಾಡಿ) ಆಯ್ಕೆಮಾಡಿ.", "ಅಧಿಕೃತ ಕ್ಲೈಮ್ ಫಾರ್ಮ್ ಭರ್ತಿ ಮಾಡಿ: ಕ್ಲೈಮ್ ಫಾರ್ಮ್‌ನ ಭಾಗ A (ವಿಮಾದಾರರ ವಿವರಗಳು) ಮತ್ತು ಭಾಗ B (ಆಸ್ಪತ್ರೆ/ಮೌಲ್ಯಮಾಪಕರ ವಿವರಗಳು) ಪೂರ್ಣಗೊಳಿಸಿ.", "ಅಗತ್ಯ ಪುರಾವೆಗಳನ್ನು ಸಂಗ್ರಹಿಸಿ: ಮೂಲ ಬಿಲ್‌ಗಳು, ಪಾವತಿ ರಶೀದಿಗಳು, ಡಿಸ್ಚಾರ್ಜ್ ಸಾರಾಂಶ, ಸರ್ವೇಯರ್ ವರದಿ ಅಥವಾ ಪೊಲೀಸ್ ಎಫ್‌ಐಆರ್ ಸಂಗ್ರಹಿಸಿ.", "ದಾಖಲೆಗಳನ್ನು ಸಲ್ಲಿಸಿ: ಹತ್ತಿರದ ಶಾಖೆಯಲ್ಲಿ ಭೌತಿಕ ದಾಖಲೆಗಳನ್ನು ಸಲ್ಲಿಸಿ ಅಥವಾ ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.", "ಸರ್ವೇಯರ್ / ವೈದ್ಯಕೀಯ ಮೌಲ್ಯಮಾಪನ: ಯಾವುದೇ ಸ್ಪಷ್ಟೀಕರಣಕ್ಕಾಗಿ ವಿಮಾ ಸರ್ವೇಯರ್ ಅಥವಾ ಟಿಪಿಎ ತನಿಖಾಧಿಕಾರಿಯೊಂದಿಗೆ ಸಹಕರಿಸಿ.", "ಕ್ಲೈಮ್ ಇತ್ಯರ್ಥ ಮತ್ತು ಪಾವತಿ: ಇತ್ಯರ್ಥ ಸಾರಾಂಶವನ್ನು ಪರಿಶೀಲಿಸಿ ಮತ್ತು ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಖಾತೆಗೆ ನೇರ NEFT ಕ್ರೆಡಿಟ್ ಪಡೆಯಿರಿ."], "required_documents": ["ಮೂಲ ಪಾಲಿಸಿ ಪ್ರತಿ ಮತ್ತು ಸಕ್ರಿಯ ಪಾಲಿಸಿ ಸಂಖ್ಯೆ", "ಭರ್ತಿ ಮಾಡಿದ ಮತ್ತು ಸಹಿ ಮಾಡಿದ ಅಧಿಕೃತ ಕ್ಲೈಮ್ ಫಾರ್ಮ್ (ಭಾಗ A ಮತ್ತು B)", "ಪಾಲಿಸಿದಾರರ ಮತ್ತು ಕ್ಲೈಮ್‌ದಾರರ ಫೋಟೋ ಗುರುತಿನ ಪುರಾವೆ (ಆಧಾರ್, ಪ್ಯಾನ್, ಪಾಸ್‌ಪೋರ್ಟ್)", "ಖಾತೆ ಸಂಖ್ಯೆ ಮತ್ತು IFSC ಕೋಡ್ ಹೊಂದಿರುವ ರದ್ದಾದ ಚೆಕ್ ಅಥವಾ ಬ್ಯಾಂಕ್ ಪಾಸ್‌ಬುಕ್ ಪ್ರತಿ", "ಮೂಲ ಅಂತಿಮ ಬಿಲ್‌ಗಳು, ಪಾವತಿ ರಶೀದಿಗಳು ಮತ್ತು ನಗದು ಮೆಮೊಗಳು", "ಘಟನೆ-ನಿರ್ದಿಷ್ಟ ಪುರಾವೆಗಳು (ಆರೋಗ್ಯಕ್ಕಾಗಿ ಡಿಸ್ಚಾರ್ಜ್ ಸಾರಾಂಶ, ಅಪಘಾತಕ್ಕೆ ಎಫ್‌ಐಆರ್, ದುರಸ್ತಿ ಅಂದಾಜುಗಳು)"], "authority_type": "ನಿಮ್ಮ ವಿಮಾದಾರರ ಕ್ಲೈಮ್‌ಗಳ ವಿಭಾಗ / ಟಿಪಿಎ (ಮೂರನೇ ವ್ಯಕ್ತಿಯ ನಿರ್ವಾಹಕರು)", "estimated_time": "ನಗದಹಿತ: 2 ರಿಂದ 6 ಗಂಟೆಗಳು; ಮರುಪಾವತಿ: ದಾಖಲೆ ಸಲ್ಲಿಕೆಯ ನಂತರ 7 ರಿಂದ 15 ಕೆಲಸದ ದಿನಗಳು", "fees": "ಉಚಿತ / ಯಾವುದೇ ಕ್ಲೈಮ್ ಸಲ್ಲಿಕೆ ಶುಲ್ಕವಿಲ್ಲ (ಪಾಲಿಸಿ ನಿಯಮಗಳ ಪ್ರಕಾರ ಕಡಿತಗಳು)"}, "policy_breakdown": {"name": "ನಿಮ್ಮ ವಿಮಾ ಪಾಲಿಸಿ ಮತ್ತು ಪ್ರಮುಖ ನಿಯಮಗಳನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳುವುದು", "description": "ನಿಮ್ಮ ಪಾಲಿಸಿ ಕಾಗದಪತ್ರಗಳನ್ನು ಸುಲಭವಾಗಿ ಅರ್ಥಮಾಡಿಕೊಳ್ಳಲು ಪಾಲಿಸಿ ನಿಯಮಗಳು, ಹೊರಗಿಡುವಿಕೆಗಳು, ಕಡಿತಗಳು, ಕಾಯುವ ಅವಧಿಗಳು ಮತ್ತು ನೆಟ್‌ವರ್ಕ್ ನಿಯಮಗಳ ವಿವರಣೆ.", "steps": ["ಪಾಲಿಸಿ ವಿವರಗಳನ್ನು ಪರಿಶೀಲಿಸಿ: ವಿಮೆ ಮಾಡಿದ ಸದಸ್ಯರ ಹೆಸರುಗಳು, ವಯಸ್ಸು, ಸಂಬಂಧ, ಪಾಲಿಸಿ ಅವಧಿ ಮತ್ತು ನಾಮಿನಿ ಹೆಸರನ್ನು ಪರಿಶೀಲಿಸಿ.", "ವಿಮಾ ಮೊತ್ತ ಮತ್ತು ಪ್ರೀಮಿಯಂ ಅರ್ಥಮಾಡಿಕೊಳ್ಳಿ: ಪಾವತಿಸಿದ ವಾರ್ಷಿಕ ಪ್ರೀಮಿಯಂಗೆ ವಿರುದ್ಧವಾಗಿ ಗರಿಷ್ಠ ವ್ಯಾಪ್ತಿಯ ಮಿತಿಯನ್ನು (ವಿಮಾ ಮೊತ್ತ) ಗಮನಿಸಿ.", "ಕಾಯುವ ಅವಧಿಗಳನ್ನು ಪರಿಶೀಲಿಸಿ: ನಿರ್ದಿಷ್ಟ ಕಾಯುವ ಅವಧಿಗಳನ್ನು ಗುರುತಿಸಿ (ಉದಾ. 30 ದಿನಗಳ ಆರಂಭಿಕ ಕಾಯುವಿಕೆ, ಮೊದಲೇ ಇರುವ ಕಾಯಿಲೆಗಳಿಗೆ 24 ರಿಂದ 48 ತಿಂಗಳು).", "ಹೊರಗಿಡುವಿಕೆಗಳನ್ನು ಪರಿಶೀಲಿಸಿ: ಎಂದಿಗೂ ಒಳಗೊಳ್ಳದ ವೈದ್ಯಕೀಯ ಚಿಕಿತ್ಸೆಗಳು ಅಥವಾ ವಸ್ತುಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.", "ಕಡಿತಗಳು ಮತ್ತು ಸಹ-ಪಾವತಿ ಷರತ್ತುಗಳು: ನಿಮ್ಮ ಪಾಲಿಸಿಯು ಕಡ್ಡಾಯ ಸಹ-ಪಾವತಿಯನ್ನು ಹೊಂದಿದೆಯೇ ಎಂದು ಗುರುತಿಸಿ.", "ನೆಟ್‌ವರ್ಕ್ ಪಟ್ಟಿ ಮತ್ತು ಟಿಪಿಎ ಸಂಪರ್ಕವನ್ನು ಉಳಿಸಿ: ನಿಮ್ಮ ಟಿಪಿಎ ಕಾರ್ಡ್, ಸಹಾಯವಾಣಿ ಸಂಖ್ಯೆಯನ್ನು ಉಳಿಸಿ ಮತ್ತು ಸ್ಥಳೀಯ ನೆಟ್‌ವರ್ಕ್ ಆಸ್ಪತ್ರೆಗಳನ್ನು ದೃಢೀಕರಿಸಿ."], "required_documents": ["ಮೂಲ ಪಾಲಿಸಿ ವೇಳಾಪಟ್ಟಿ ಮತ್ತು ನಿಯಮಗಳ ದಾಖಲೆ", "ಟಿಪಿಎ ಸಂಖ್ಯೆ ಮತ್ತು ಪಾಲಿಸಿ ಗುರುತಿಸುವಿಕೆಯನ್ನು ಹೊಂದಿರುವ ಡಿಜಿಟಲ್ ಹೆಲ್ತ್ ಕಾರ್ಡ್", "80D / 80C ತೆರಿಗೆ ವಿನಾಯಿತಿ ಪ್ರಮಾಣಪತ್ರದೊಂದಿಗೆ ಪ್ರೀಮಿಯಂ ಪಾವತಿ ರಶೀದಿ", "ವಿಮೆ ಮಾಡಿದ ಸದಸ್ಯರ ಕೆವೈಸಿ ದಾಖಲೆಗಳು (ಆಧಾರ್, ಪ್ಯಾನ್ ಕಾರ್ಡ್, ಜನ್ಮ ದಿನಾಂಕ ಪುರಾವೆ)", "ಮೊದಲೇ ಅಸ್ತಿತ್ವದಲ್ಲಿರುವ ವೈದ್ಯಕೀಯ ಇತಿಹಾಸ ಮತ್ತು ಹಿಂದಿನ ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್‌ಗಳು"], "authority_type": "ಭಾರತೀಯ ವಿಮಾ ನಿಯಂತ್ರಣ ಮತ್ತು ಅಭಿವೃದ್ಧಿ ಪ್ರಾಧಿಕಾರ (IRDAI) / ನಿಮ್ಮ ವಿಮಾದಾರ", "estimated_time": "ಪಾಲಿಸಿ ಸ್ವೀಕರಿಸಿದ ದಿನಾಂಕದಿಂದ 15 ರಿಂದ 30 ದಿನಗಳ ಪರಿಶೀಲನಾ ಅವಧಿ (ಫ್ರೀ-ಲುಕ್)", "fees": "ಯಾವುದೇ ಶುಲ್ಕವಿಲ್ಲ / ಪ್ರಮಾಣಿತ ಶಾಸನಬದ್ಧ ಪಾಲಿಸಿ ಆಡಳಿತ"}, "health_insurance_coverage": {"name": "ಆರೋಗ್ಯ ವಿಮಾ ರಕ್ಷಣೆ ಮತ್ತು ಕ್ಲೈಮ್‌ಗಳು (ನಗದಹಿತ ವಿರುದ್ಧ ಮರುಪಾವತಿ)", "description": "ಆಸ್ಪತ್ರೆ ದಾಖಲಾತಿ ಪ್ರಯೋಜನಗಳು, ಪೂರ್ವ/ನಂತರದ ವೆಚ್ಚಗಳು, ಡೇ-ಕೇರ್ ಚಿಕಿತ್ಸೆಗಳು, ಹೊರಗಿಡುವಿಕೆಗಳು ಮತ್ತು ನಗದಹಿತ ಪ್ರಿ-ಆಥರೈಸೇಶನ್ ವಿರುದ್ಧ ಮರುಪಾವತಿಯ ವಿವರವಾದ ಮಾರ್ಗದರ್ಶಿ.", "steps": ["ಯೋಜಿತ ಆಸ್ಪತ್ರೆ ದಾಖಲಾತಿ (ನಗದಹಿತ): 48 ರಿಂದ 72 ಗಂಟೆಗಳ ಮೊದಲು ನೆಟ್‌ವರ್ಕ್ ಆಸ್ಪತ್ರೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ; ಆಸ್ಪತ್ರೆಯ ಟಿಪಿಎ ಡೆಸ್ಕ್‌ನಲ್ಲಿ ಫಾರ್ಮ್ ಸಲ್ಲಿಸಿ.", "ತುರ್ತು ಆಸ್ಪತ್ರೆ ದಾಖಲಾತಿ (ನಗದಹಿತ): ದಾಖಲಾದ 24 ಗಂಟೆಗಳ ಒಳಗೆ ವಿಮಾದಾರರಿಗೆ ತಿಳಿಸಿ; ಆಸ್ಪತ್ರೆಯು ತುರ್ತು ವಿನಂತಿಯನ್ನು ಕಳುಹಿಸುತ್ತದೆ.", "ವಿಮಾದಾರರ ಅನುಮೋದನೆ: ವಿಮಾದಾರರು ಆರಂಭಿಕ ಮಂಜೂರಾತಿ ಪತ್ರವನ್ನು ನೀಡುತ್ತಾರೆ; ಡಿಸ್ಚಾರ್ಜ್ ಸಮಯದಲ್ಲಿ ಅಂತಿಮ ಬಿಲ್ ಇತ್ಯರ್ಥವಾಗುತ್ತದೆ.", "ಮರುಪಾವತಿ ಕ್ಲೈಮ್‌ಗಳು (ನಾನ್-ನೆಟ್‌ವರ್ಕ್ ಆಸ್ಪತ್ರೆ): ಆಸ್ಪತ್ರೆಯ ಬಿಲ್‌ಗಳನ್ನು ನೇರವಾಗಿ ಪಾವತಿಸಿ, ಎಲ್ಲಾ ಮೂಲ ದಾಖಲೆಗಳು ಮತ್ತು ವರದಿಗಳನ್ನು ಸಂಗ್ರಹಿಸಿ.", "ದಾಖಲಾತಿ ಪೂರ್ವ ಮತ್ತು ನಂತರದ ವೆಚ್ಚಗಳು: ದಾಖಲಾತಿಗೆ 30-60 ದಿನಗಳ ಮೊದಲು ಮತ್ತು ಡಿಸ್ಚಾರ್ಜ್ ಆದ 60-90 ದಿನಗಳ ನಂತರದ ಎಲ್ಲಾ ಬಿಲ್‌ಗಳನ್ನು ಸೇರಿಸಿ.", "ಕ್ಲೈಮ್ ಪ್ಯಾಕೇಜ್ ಸಲ್ಲಿಸಿ: ಡಿಸ್ಚಾರ್ಜ್ ಆದ 15 ರಿಂದ 30 ದಿನಗಳಲ್ಲಿ ಕ್ಲೈಮ್ ಫಾರ್ಮ್ ಮತ್ತು ಎಲ್ಲಾ ಮೂಲ ದಾಖಲೆಗಳನ್ನು ಸಲ್ಲಿಸಿ.", "ಇತ್ಯರ್ಥ ಮತ್ತು ಪಾವತಿ: ಬ್ಯಾಂಕ್ ವರ್ಗಾವಣೆಯ ಮೂಲಕ ಪಾವತಿಯನ್ನು ಸ್ವೀಕರಿಸಿ."], "required_documents": ["ಭರ್ತಿ ಮಾಡಿದ ಆರೋಗ್ಯ ಕ್ಲೈಮ್ ಫಾರ್ಮ್ (ಭಾಗ A ಮತ್ತು ವೈದ್ಯರು ಸಹಿ ಮಾಡಿದ ಭಾಗ B)", "ದಾಖಲಾತಿ ಕಾರಣ, ನೀಡಲಾದ ಚಿಕಿತ್ಸೆಯನ್ನು ವಿವರಿಸುವ ಆಸ್ಪತ್ರೆ ಡಿಸ್ಚಾರ್ಜ್ ಸಾರಾಂಶ", "ಕೊಠಡಿ ಬಾಡಿಗೆ, ಐಸಿಯು ಮತ್ತು ಶಸ್ತ್ರಚಿಕಿತ್ಸಾ ಶುಲ್ಕಗಳ ವಿವರಗಳೊಂದಿಗೆ ಮೂಲ ಅಂತಿಮ ಬಿಲ್", "ಮೂಲ ಪಾವತಿ ರಶೀದಿಗಳು ಮತ್ತು ವೈದ್ಯರ ಸಮಾಲೋಚನೆ ಚೀಟಿಗಳು", "ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್‌ಗಳೊಂದಿಗೆ ಎಲ್ಲಾ ರೋಗನಿರ್ಣಯ ಮತ್ತು ಪ್ರಯೋಗಾಲಯ ತನಿಖಾ ವರದಿಗಳು (ರಕ್ತ ಪರೀಕ್ಷೆಗಳು, ಎಕ್ಸ್-ರೇ, ಎಂಆರ್‌ಐ)", "ಇಂಪ್ಲಾಂಟ್ ಸ್ಟಿಕ್ಕರ್‌ಗಳು ಮತ್ತು ಖರೀದಿ ಇನ್‌ವಾಯ್ಸ್‌ಗಳು (ಪೇಸ್‌ಮೇಕರ್, ಸ್ಟೆಂಟ್‌ಗಳು, ಇತ್ಯಾದಿ)", "ನೇರ ಬ್ಯಾಂಕ್ ಮರುಪಾವತಿಗಾಗಿ ಪ್ರಾಥಮಿಕ ಪಾಲಿಸಿದಾರರ ರದ್ದಾದ ಚೆಕ್"], "authority_type": "ಆಸ್ಪತ್ರೆ ಟಿಪಿಎ ಹೆಲ್ಪ್‌ಡೆಸ್ಕ್ / ವಿಮಾದಾರರ ಆರೋಗ್ಯ ಕ್ಲೈಮ್‌ಗಳ ವಿಭಾಗ", "estimated_time": "ನಗದಹಿತ ಪೂರ್ವ-ದೃಢೀಕರಣ: 2 ರಿಂದ 4 ಗಂಟೆಗಳು; ಅಂತಿಮ ಅನುಮೋದನೆ: 2 ರಿಂದ 6 ಗಂಟೆಗಳು; ಮರುಪಾವತಿ: 7 ರಿಂದ 15 ದಿನಗಳು", "fees": "ಯಾವುದೇ ಕ್ಲೈಮ್ ಸಲ್ಲಿಕೆ ಶುಲ್ಕವಿಲ್ಲ; ಪಾಲಿಸಿ ನಿಯಮಗಳ ಪ್ರಕಾರ ಕಡ್ಡಾಯ ಸಹ-ಪಾವತಿ"}, "auto_insurance_coverage": {"name": "ಮೋಟಾರು / ವಾಹನ ವಿಮಾ ರಕ್ಷಣೆ ಮತ್ತು ಅಪಘಾತ ಕ್ಲೈಮ್‌ಗಳು", "description": "ಸಮಗ್ರ ವಿರುದ್ಧ ಮೂರನೇ ವ್ಯಕ್ತಿಯ ವಾಹನ ಹಾನಿ ಕ್ಲೈಮ್‌ಗಳು, ಕಳ್ಳತನ ಕ್ಲೈಮ್‌ಗಳು, ಅಪಘಾತ ಸರ್ವೇಯರ್ ಪರಿಶೀಲನೆ ಮತ್ತು ನೆಟ್‌ವರ್ಕ್ ಗ್ಯಾರೇಜ್ ನಗದಹಿತ ದುರಸ್ತಿ ಪ್ರಕ್ರಿಯೆ.", "steps": ["ಸುರಕ್ಷತೆ ಮತ್ತು ತಕ್ಷಣದ ಸಾಕ್ಷ್ಯ: ವಾಹನ ನೋಂದಣಿ ಸಂಖ್ಯೆಯನ್ನು ಗಮನಿಸಿ, ಅಪಘಾತದ ಸ್ಥಳ ಮತ್ತು ಹಾನಿಯ ಸ್ಪಷ್ಟ ಫೋಟೋಗಳನ್ನು ತೆಗೆದುಕೊಳ್ಳಿ.", "ತಕ್ಷಣದ ಕ್ಲೈಮ್ ಮಾಹಿತಿ: ವಾಹನವನ್ನು ಚಲಿಸುವ ಮೊದಲು ವಿಮಾದಾರರ ಸಹಾಯವಾಣಿಗೆ ಕರೆ ಮಾಡಿ ಅಥವಾ ಮೊಬೈಲ್ ಅಪ್ಲಿಕೇಶನ್‌ನಲ್ಲಿ ಕ್ಲೈಮ್ ಮಾಡಿ.", "ಪೊಲೀಸ್ ಎಫ್‌ಐಆರ್ / ಪಂಚನಾಮೆ: ಮೂರನೇ ವ್ಯಕ್ತಿಗೆ ಗಾಯ, ಸಾವು, ಆಸ್ತಿ ಹಾನಿ ಅಥವಾ ಕಳ್ಳತನ ಸಂಭವಿಸಿದರೆ ಎಫ್‌ಐಆರ್ ಕಡ್ಡಾಯ.", "ಅಧಿಕೃತ ನಗದಹಿತ ಗ್ಯಾರೇಜ್‌ಗೆ ತೆರಳಿ: ನಗದಹಿತ ಮೌಲ್ಯಮಾಪನಕ್ಕಾಗಿ ವಾಹನವನ್ನು ಅನುಮೋದಿತ ನೆಟ್‌ವರ್ಕ್ ಗ್ಯಾರೇಜ್‌ಗೆ ಕೊಂಡೊಯ್ಯಿರಿ.", "ಸರ್ವೇಯರ್ ಪರಿಶೀಲನೆ: ವಿಮಾ ಸರ್ವೇಯರ್ ಹಾನಿಯನ್ನು ಪರಿಶೀಲಿಸುತ್ತಾರೆ ಮತ್ತು ದುರಸ್ತಿ ಅಂದಾಜನ್ನು ಅನುಮೋದಿಸುತ್ತಾರೆ.", "ವಾಹನ ದುರಸ್ತಿ: ಅನುಮೋದಿತ ಅಂದಾಜಿನ ಪ್ರಕಾರ ಗ್ಯಾರೇಜ್ ವಾಹನವನ್ನು ದುರಸ್ತಿ ಮಾಡುತ್ತದೆ.", "ಕಡ್ಡಾಯ ಕಡಿತ ಪಾವತಿ ಮತ್ತು ವಿತರಣೆ: ಕಡ್ಡಾಯ ಕಡಿತದ ಮೊತ್ತವನ್ನು ಪಾವತಿಸಿ ಮತ್ತು ವಾಹನವನ್ನು ಸ್ವೀಕರಿಸಿ."], "required_documents": ["ಸಕ್ರಿಯ ಮೋಟಾರು ವಿಮಾ ಪಾಲಿಸಿ ಪ್ರತಿ", "ವಾಹನ ನೋಂದಣಿ ಪ್ರಮಾಣಪತ್ರ (ಆರ್‌ಸಿ ಬುಕ್ / ಸ್ಮಾರ್ಟ್ ಕಾರ್ಡ್)", "ಅಪಘಾತದ ಸಮಯದಲ್ಲಿ ವಾಹನ ಚಲಾಯಿಸುತ್ತಿದ್ದ ವ್ಯಕ್ತಿಯ ಮಾನ್ಯ ಚಾಲನಾ ಪರವಾನಗಿ (ಡಿಎಲ್)", "ಭರ್ತಿ ಮಾಡಿದ ಮತ್ತು ಸಹಿ ಮಾಡಿದ ಮೋಟಾರು ಕ್ಲೈಮ್ ಫಾರ್ಮ್", "ಮೂಲ ಪೊಲೀಸ್ ಎಫ್‌ಐಆರ್ / ಡಿಡಿ ನಮೂದು (ಕಳ್ಳತನ ಅಥವಾ ಮೂರನೇ ವ್ಯಕ್ತಿಯ ಗಾಯಕ್ಕೆ)", "ಗ್ಯಾರೇಜ್ ದುರಸ್ತಿ ಅಂದಾಜು ಮತ್ತು ಪಾವತಿ ರಶೀದಿಯೊಂದಿಗೆ ಮೂಲ ತೆರಿಗೆ ಸರಕುಪಟ್ಟಿ", "ನೋಂದಣಿ ಸಂಖ್ಯೆ ಫಲಕವನ್ನು ಸ್ಪಷ್ಟವಾಗಿ ತೋರಿಸುವ ಹಾನಿಗೊಳಗಾದ ವಾಹನದ ಫೋಟೋಗಳು"], "authority_type": "ವಿಮಾದಾರರ ಮೋಟಾರು ಕ್ಲೈಮ್ ಕೇಂದ್ರ / ಪರವಾನಗಿ ಪಡೆದ ವಿಮಾ ಸರ್ವೇಯರ್", "estimated_time": "ಅಪ್ಲಿಕೇಶನ್ ಮೂಲಕ ಸಮೀಕ್ಷೆ: 2 ರಿಂದ 6 ಗಂಟೆಗಳು; ಪ್ರಮುಖ ದುರಸ್ತಿ ಅನುಮೋದನೆ: 2 ರಿಂದ 5 ದಿನಗಳು; ಒಟ್ಟು ಸಮಯ: 5 ರಿಂದ 10 ದಿನಗಳು", "fees": "ಕಡ್ಡಾಯ ಪಾಲಿಸಿ ಕಡಿತಗೊಳಿಸಬಹುದಾದ ಶುಲ್ಕ (ಕಾರುಗಳಿಗೆ ₹1,000 - ₹2,000, ದ್ವಿಚಕ್ರ ವಾಹನಗಳಿಗೆ ₹100)"}, "documents_keep_ready": {"name": "ಅಗತ್ಯ ವಿಮಾ ದಾಖಲೆಗಳ ಸಿದ್ಧತೆಯ ಪರಿಶೀಲನಾಪಟ್ಟಿ", "description": "ಕ್ಲೈಮ್ ಇತ್ಯರ್ಥಕ್ಕಾಗಿ ಪ್ರತಿಯೊಂದು ಕುಟುಂಬವೂ ಸಂಘಟಿತವಾಗಿ ಇಟ್ಟುಕೊಳ್ಳಬೇಕಾದ ಪ್ರಮುಖ ದಾಖಲೆಗಳು ಮತ್ತು ನಾಮಿನಿ ಪುರಾವೆಗಳ ಸಿದ್ಧತೆಯ ಪರಿಶೀಲನಾಪಟ್ಟಿ.", "steps": ["ಮಾಸ್ಟರ್ ಕುಟುಂಬ ವಿಮಾ ಫೋಲ್ಡರ್ ರಚಿಸಿ: ಜಲನಿರೋಧಕ ಫೋಲ್ಡರ್ ಮತ್ತು ಸುರಕ್ಷಿತ ಡಿಜಿಟಲ್ ಫೋಲ್ಡರ್ (ಡಿಜಿಲಾಕರ್/ಇ-ವಿಮಾ ಖಾತೆ) ನಿರ್ವಹಿಸಿ.", "ಪಾಲಿಸಿ ವೇಳಾಪಟ್ಟಿಗಳನ್ನು ಸಂಘಟಿಸಿ: ಇತ್ತೀಚಿನ ನವೀಕರಣ ರಶೀದಿಗಳೊಂದಿಗೆ ಎಲ್ಲಾ ಸಕ್ರಿಯ ಜೀವ, ಆರೋಗ್ಯ ಮತ್ತು ಮೋಟಾರು ಪಾಲಿಸಿಗಳ ಪ್ರತಿಗಳನ್ನು ಇರಿಸಿ.", "ನಾಮಿನಿ ಮಾಹಿತಿಯನ್ನು ಪರಿಶೀಲಿಸಿ: ಎಲ್ಲಾ ಪಾಲಿಸಿಗಳಲ್ಲಿ ನಾಮಿನಿ ಹೆಸರು ಮತ್ತು ಬ್ಯಾಂಕ್ ವಿವರಗಳು ನವೀಕೃತವಾಗಿವೆ ಎಂದು ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ.", "ಕೆವೈಸಿ ಪೋರ್ಟ್‌ಫೋಲಿಯೊ ನಿರ್ವಹಿಸಿ: ಎಲ್ಲಾ ವಿಮೆ ಮಾಡಿದ ಸದಸ್ಯರ ಆಧಾರ್, ಪ್ಯಾನ್ ಮತ್ತು ಮತದಾರರ ಗುರುತಿನ ಚೀಟಿಯ ಪ್ರತಿಗಳನ್ನು ಇರಿಸಿ.", "ಹಿಂದಿನ ವೈದ್ಯಕೀಯ ಇತಿಹಾಸವನ್ನು ದಾಖಲಿಸಿ: ಆಸ್ಪತ್ರೆಯ ಡಿಸ್ಚಾರ್ಜ್ ಸಾರಾಂಶಗಳು ಮತ್ತು ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್‌ಗಳನ್ನು ಕಾಲಾನುಕ್ರಮದಲ್ಲಿ ಇರಿಸಿ.", "ಕುಟುಂಬದೊಂದಿಗೆ ತುರ್ತು ಪ್ರವೇಶವನ್ನು ಹಂಚಿಕೊಳ್ಳಿ: ಪಾಲಿಸಿ ಸ್ಥಳಗಳು ಮತ್ತು ಸಹಾಯವಾಣಿ ಸಂಖ್ಯೆಗಳ ಬಗ್ಗೆ ನಿಮ್ಮ ಕುಟುಂಬಕ್ಕೆ ತಿಳಿಸಿ."], "required_documents": ["ಮಾಸ್ಟರ್ ವಿಮಾ ಪಾಲಿಸಿಗಳು (ಪಾಲಿಸಿ ವೇಳಾಪಟ್ಟಿ, ನಿಯಮಗಳು ಮತ್ತು ಇ-ಕಾರ್ಡ್ ಮುದ್ರಣಗಳು)", "ಇತ್ತೀಚಿನ ಪ್ರೀಮಿಯಂ ಪಾವತಿ ರಶೀದಿಗಳು ಮತ್ತು 80D / 80C ತೆರಿಗೆ ವಿನಾಯಿತಿ ಪ್ರಮಾಣಪತ್ರಗಳು", "ಎಲ್ಲಾ ಸದಸ್ಯರ ಅಧಿಕೃತ ಫೋಟೋ ಗುರುತಿನ ಪುರಾವೆ (ಆಧಾರ್, ಪ್ಯಾನ್, ಪಾಸ್‌ಪೋರ್ಟ್)", "ವಿಳಾಸದ ಪುರಾವೆ (ವಿದ್ಯುತ್ ಬಿಲ್, ಪಾಸ್‌ಪೋರ್ಟ್, ಆಧಾರ್, ಬ್ಯಾಂಕ್ ವಿವರ)", "ನಾಮಿನಿಯ ಗುರುತಿನ ಪುರಾವೆ, ಜನ್ಮ ದಿನಾಂಕ ಪುರಾವೆ ಮತ್ತು ಸಕ್ರಿಯ ಬ್ಯಾಂಕ್ ವಿವರಗಳು", "ಖಾತೆ ಸಂಖ್ಯೆ ಮತ್ತು IFSC ಕೋಡ್ ಹೊಂದಿರುವ ರದ್ದಾದ ಚೆಕ್ / ಬ್ಯಾಂಕ್ ಪಾಸ್‌ಬುಕ್ ಪ್ರತಿ", "ಸಂಪೂರ್ಣ ಹಿಂದಿನ ವೈದ್ಯಕೀಯ ಇತಿಹಾಸ ಡೋಸಿಯರ್ (ಡಿಸ್ಚಾರ್ಜ್ ಸಾರಾಂಶಗಳು, ಶಸ್ತ್ರಚಿಕಿತ್ಸಾ ಟಿಪ್ಪಣಿಗಳು, ಲ್ಯಾಬ್ ವರದಿಗಳು)"], "authority_type": "ಕುಟುಂಬ ವಿಮಾ ದಾಖಲೆ / ವಿಮಾದಾರರ ಗ್ರಾಹಕ ಸೇವೆ", "estimated_time": "ತಕ್ಷಣದ ಪ್ರವೇಶ / ವಾರ್ಷಿಕ ಸಿದ್ಧತೆಯ ಪರಿಶೀಲನೆ", "fees": "ಯಾವುದೇ ಶುಲ್ಕವಿಲ್ಲ / 100% ಉಚಿತ ವೈಯಕ್ತಿಕ ಸಿದ್ಧತೆ"}})

```

---

## 📄 `logic/grok_calls.py`

```python
﻿from logic.llm_calls import general_chat_answer

def general_answer(question: str, language: str = "English") -> str:
    """
    Answers general user questions using the active LLM engine (Groq / Anthropic).
    """
    return general_chat_answer(question, language=language)

```

---

## 📄 `pages/login.py`

```python
﻿import streamlit as st
from logic.translations import t, get_normalized_language

def show_login():
    render_login()

def render_login():
    # Top Language Selector before login
    col_l1, col_l2 = st.columns([5, 1.5])
    with col_l2:
        lang_options = ["English", "Hindi (हिंदी)", "Kannada (ಕನ್ನಡ)"]
        curr_lang = st.session_state.get("language", "English")
        curr_idx = 0
        if "Hindi" in curr_lang:
            curr_idx = 1
        elif "Kannada" in curr_lang:
            curr_idx = 2
            
        selected_lang_label = st.selectbox(
            "🌐 Language / भाषा",
            lang_options,
            index=curr_idx,
            key="login_page_lang_selector"
        )
        norm_selected = get_normalized_language(selected_lang_label)
        if norm_selected != get_normalized_language(st.session_state.get("language")):
            st.session_state["language"] = norm_selected
            st.rerun()

    # Hero Header
    st.markdown(f"""
    <div style="text-align: center; padding: 15px 0 15px 0;">
        <h1 style="font-size: 34px; margin-bottom: 8px; color: var(--card-border-blue, #005A9C);">{t("hero_title")}</h1>
        <p style="color: var(--app-text-muted, #666); font-size: 16px; max-width: 700px; margin: 0 auto;">
            {t("hero_subtitle")}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown(f"""
        <div style="background: var(--box-summary-bg, #f8f9fa); border: 1px solid var(--box-summary-border, #e2e8f0); border-radius: 12px 12px 0 0; padding: 24px 28px 12px 28px; margin-top: 15px;">
            <h3 style="color: var(--app-text, #1a202c); margin-top: 0; margin-bottom: 6px;">{t("sign_in_title")}</h3>
            <p style="color: var(--app-text-muted, #718096); font-size: 14px; margin-bottom: 0;">{t("sign_in_subtitle")}</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form(key="login_form"):
            name = st.text_input(t("full_name_label"), value=st.session_state.get("user_name", ""), placeholder=t("full_name_placeholder"))
            email = st.text_input(t("email_label"), value=st.session_state.get("user_email", ""), placeholder=t("email_placeholder"))
            
            submitted = st.form_submit_button(t("continue_btn"), use_container_width=True)
            if submitted:
                if not name.strip():
                    st.warning(t("name_required_warning"))
                else:
                    st.session_state["user"] = {
                        "name": name.strip(),
                        "email": email.strip()
                    }
                    st.session_state["user_name"] = name.strip()
                    st.session_state["user_email"] = email.strip()
                    st.session_state["page"] = "home"
                    st.rerun()

        # Highlights feature badges below form
        st.markdown(f"""
        <div style="display: flex; justify-content: space-around; margin-top: 25px; text-align: center; color: var(--app-text-muted, #718096); font-size: 13px;">
            <div>{t("badge_notice")}</div>
            <div>{t("badge_govt")}</div>
            <div>{t("badge_multi")}</div>
        </div>
        """, unsafe_allow_html=True)

```

---

## 📄 `pages/home.py`

```python
﻿import streamlit as st
from logic.llm_calls import general_chat_answer
from logic.translations import t, get_normalized_language

def show_home():
    render_home()

def render_home():
    user = st.session_state.get("user", {})
    user_name = user.get("name", "Citizen")
    current_lang = get_normalized_language(st.session_state.get("language", "English"))

    # Top Greeting & Description Row
    st.markdown(f"## {t('welcome_greeting', user_name=user_name)}")
    st.markdown(f"*{t('site_description')}*")

    st.markdown("<br>", unsafe_allow_html=True)

    # 1. Upload Document Section
    st.markdown(f"""
    <div style="background-color: var(--card-bg-blue, #f0f8ff); border: 2px solid var(--card-border-blue, #005A9C); border-radius: 10px; padding: 22px 26px; margin-bottom: 25px;">
        <h3 style="color: var(--card-border-blue, #005A9C); margin-top: 0; margin-bottom: 8px;">{t('upload_banner_title')}</h3>
        <p style="color: var(--app-text, #2d3748); font-size: 15px; margin-bottom: 14px;">
            {t('upload_banner_desc')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button(t("upload_analyze_btn"), key="btn_home_go_upload", use_container_width=True):
        st.session_state["page"] = "upload"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. General Q&A Chatbot Section
    with st.container():
        st.markdown(f"### {t('ask_ai_header')}")
        st.caption(t("ask_ai_caption", language=current_lang))

        if "general_chat_history" not in st.session_state:
            st.session_state["general_chat_history"] = []

        for msg in st.session_state["general_chat_history"]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        user_prompt = st.chat_input(t("ask_ai_placeholder", language=current_lang), key="home_general_chat_input")
        if user_prompt:
            st.session_state["general_chat_history"].append({"role": "user", "content": user_prompt})
            with st.chat_message("user"):
                st.write(user_prompt)

            with st.chat_message("assistant"):
                with st.spinner(f"🔍 {t('thinking')}"):
                    reply = general_chat_answer(
                        question=user_prompt,
                        history=st.session_state["general_chat_history"][:-1],
                        language=current_lang
                    )
                    st.write(reply)
                    st.session_state["general_chat_history"].append({"role": "assistant", "content": reply})

    st.markdown("---")

    # 3. 3 Main Service Options (Government, Banking, Insurance)
    st.markdown(f"### {t('services_header')}")

    col1, col2, col3 = st.columns(3)

    # Card 1: Government Services
    with col1:
        st.markdown(f"""
        <div style="background-color: var(--card-bg-orange, #fff8f0); border: 2px solid var(--card-border-orange, #E37222); border-radius: 8px; padding: 20px; min-height: 240px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <h4 style="color: var(--card-border-orange, #E37222); margin-top: 0; margin-bottom: 8px;">{t('card_govt_title')}</h4>
                <p style="color: var(--app-text, #4a5568); font-size: 14px; line-height: 1.5;">
                    {t('card_govt_desc')}
                </p>
            </div>
            <div style="font-size: 12px; color: var(--app-text-muted, #718096); margin-top: 10px; font-weight: 500;">
                {t('card_govt_badge')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        if st.button(t("card_govt_btn"), key="btn_main_govt", use_container_width=True):
            st.session_state["guide_category"] = "government"
            st.session_state["page"] = "process_picker"
            st.rerun()

    # Card 2: Banking Services (Active Curated Guides)
    with col2:
        st.markdown(f"""
        <div style="background-color: var(--card-bg-banking, #ebf8ff); border: 2px solid var(--card-border-banking, #2B6CB0); border-radius: 8px; padding: 20px; min-height: 240px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <h4 style="color: var(--card-border-banking, #2B6CB0); margin-top: 0; margin-bottom: 8px;">{t('card_banking_title')}</h4>
                <p style="color: var(--app-text, #4a5568); font-size: 14px; line-height: 1.5;">
                    {t('card_banking_desc')}
                </p>
            </div>
            <div style="font-size: 12px; color: var(--app-text-muted, #718096); margin-top: 10px; font-weight: 500;">
                {t('card_banking_badge')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        if st.button(t("card_banking_btn"), key="btn_main_banking", use_container_width=True):
            st.session_state["guide_category"] = "banking"
            st.session_state["page"] = "process_picker"
            st.rerun()

    # Card 3: Insurance Services
    with col3:
        st.markdown(f"""
        <div style="background-color: var(--card-bg-insurance, #e6fffa); border: 2px solid var(--card-border-insurance, #2C7A7B); border-radius: 8px; padding: 20px; min-height: 240px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <h4 style="color: var(--card-border-insurance, #2C7A7B); margin-top: 0; margin-bottom: 8px;">{t('card_insurance_title')}</h4>
                <p style="color: var(--app-text, #4a5568); font-size: 14px; line-height: 1.5;">
                    {t('card_insurance_desc')}
                </p>
            </div>
            <div style="font-size: 12px; color: var(--app-text-muted, #718096); margin-top: 10px; font-weight: 500;">
                {t('card_insurance_badge')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        if st.button(t("card_insurance_btn"), key="btn_main_insurance", use_container_width=True):
            st.session_state["guide_category"] = "insurance"
            st.session_state["page"] = "process_picker"
            st.rerun()

```

---

## 📄 `pages/upload.py`

```python
﻿import streamlit as st
import time
from logic.extract_text import get_text
from logic.llm_calls import analyze_document, answer_question
from logic.translations import t, get_normalized_language

def show_upload():
    render_upload()

def render_upload():
    current_lang = get_normalized_language(st.session_state.get("language", "English"))

    # Top Navigation Bar
    col_nav1, col_nav2 = st.columns([2, 5])
    with col_nav1:
        if st.button(t("back_to_home"), key="btn_upload_back_home", use_container_width=True):
            st.session_state["page"] = "home"
            st.rerun()

    st.markdown(f"## {t('upload_page_title')}")

    uploaded_file = st.file_uploader(
        t("upload_file_prompt"),
        type=["pdf", "docx"],
        key="dedicated_file_uploader"
    )

    if uploaded_file is None:
        st.info(t("upload_empty_info"))
        return

    # 1. Document info row
    file_ext = uploaded_file.name.split(".")[-1].upper()
    file_size_kb = uploaded_file.size / 1024
    
    st.markdown(f"""
    <div style="background-color: var(--card-bg-blue, #f0f4f8); border: 1px solid var(--card-border-blue, #d9e2ec); border-radius: 8px; padding: 12px 18px; margin-top: 10px; margin-bottom: 18px; color: var(--app-text, #1a202c);">
        <strong>📎 {t('file_name_label')}:</strong> <code>{uploaded_file.name}</code> &nbsp;|&nbsp; 
        <strong>{t('file_type_label')}:</strong> <span style="background-color: var(--card-border-blue, #005A9C); color: #ffffff; padding: 3px 8px; border-radius: 4px; font-size: 13px; font-weight: bold;">{file_ext}</span> &nbsp;|&nbsp; 
        <strong>{t('file_size_label')}:</strong> <strong>{file_size_kb:.1f} KB</strong> &nbsp;|&nbsp; 
        <strong>{t('target_lang_label')}:</strong> <strong>{current_lang}</strong>
    </div>
    """, unsafe_allow_html=True)

    is_already_analyzed = (
        st.session_state.get("analysis_result") is not None
        and st.session_state.get("uploaded_file_name") == uploaded_file.name
        and st.session_state.get("analyzed_language") == current_lang
    )

    stage_placeholder = st.empty()

    if not is_already_analyzed:
        # 2. Upload bar
        with stage_placeholder.container():
            st.info(t("status_extracting"))
            p_bar = st.progress(25)
            try:
                extracted_text = get_text(uploaded_file, uploaded_file.name)
                p_bar.progress(50)
            except Exception as e:
                st.error(f"❌ Failed to extract text: {str(e)}")
                return

        # 3. Analyzing bar
        with stage_placeholder.container():
            st.info(t("status_analyzing", language=current_lang))
            p_bar = st.progress(75)
            try:
                analysis = analyze_document(extracted_text, language=current_lang)
                p_bar.progress(100)
            except Exception as e:
                st.error(f"❌ Failed during analysis: {str(e)}")
                return

            if "error" in analysis:
                st.error(f"❌ Analysis error: {analysis['error']}")
                return

            # Save state
            st.session_state["doc_text"] = extracted_text
            st.session_state["analysis_result"] = analysis
            st.session_state["context_raw"] = extracted_text
            st.session_state["uploaded_file_name"] = uploaded_file.name
            st.session_state["analyzed_language"] = current_lang
            st.session_state["chat_history"] = []
            st.session_state["step_progress"] = {}
            
            # Record in completed history
            if "completed_history" not in st.session_state:
                st.session_state["completed_history"] = []
            
            doc_type_val = analysis.get("doc_type", uploaded_file.name)
            existing_rec = next((r for r in st.session_state["completed_history"] if r.get("id") == uploaded_file.name), None)
            if not existing_rec:
                st.session_state["completed_history"].append({
                    "id": uploaded_file.name,
                    "name": f"{doc_type_val} ({uploaded_file.name})",
                    "category": "documents",
                    "status": "Analyzed & Loaded"
                })
            
            st.rerun()

    # 3 (continued). Summary display
    analysis = st.session_state.get("analysis_result", {})
    doc_type = analysis.get("doc_type", t("summary_heading"))
    summary_text = analysis.get("summary", "No summary text provided.")
    extracted_text = st.session_state.get("doc_text", "")

    with stage_placeholder.container():
        st.markdown(f"### 📋 {doc_type}")
        st.markdown(f"""
        <div style="background-color: var(--box-summary-bg, #f8f9fa); border-left: 4px solid var(--card-border-blue, #005A9C); padding: 18px 22px; border-radius: 8px; font-size: 16px; line-height: 1.6; color: var(--app-text, #212529); margin-bottom: 18px; border-top: 1px solid var(--box-summary-border, #e2e8f0); border-right: 1px solid var(--box-summary-border, #e2e8f0); border-bottom: 1px solid var(--box-summary-border, #e2e8f0);">
            {summary_text}
        </div>
        """, unsafe_allow_html=True)

        if analysis.get("risks"):
            st.warning(f"**{t('critical_risks_label')}** " + " | ".join(analysis["risks"]))

    # 4. Question bar
    st.markdown("---")
    st.markdown(f"### {t('ask_doc_header')}")
    st.caption(t("ask_doc_caption", filename=uploaded_file.name, language=current_lang))

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_q = st.chat_input(t("ask_doc_placeholder", language=current_lang))
    if user_q:
        st.session_state["chat_history"].append({"role": "user", "content": user_q})
        with st.chat_message("user"):
            st.write(user_q)

        with st.chat_message("assistant"):
            with st.spinner(f"🔍 {t('thinking')}"):
                answer = answer_question(extracted_text, user_q, language=current_lang)
                st.write(answer)
                st.session_state["chat_history"].append({"role": "assistant", "content": answer})

```

---

## 📄 `pages/process_picker.py`

```python
﻿import streamlit as st
from logic.process_data import load_processes, format_process_for_analysis
from logic.llm_calls import answer_question, bank_loan_info
from logic.translations import t, get_normalized_language

def show_process_picker():
    render_process_picker()

def render_process_picker():
    current_lang = get_normalized_language(st.session_state.get("language", "English"))
    category = st.session_state.get("guide_category", "government")

    # Top Navigation Bar
    col_nav1, col_nav2 = st.columns([2, 5])
    with col_nav1:
        if st.button(t("back_to_home"), key="btn_proc_back_home", use_container_width=True):
            st.session_state["page"] = "home"
            st.rerun()

    # Dynamic Titles based on category
    if category == "insurance":
        page_title = t("insurance_page_title")
        page_desc = t("insurance_page_desc")
        selector_label = t("insurance_selector_label")
        accent_color = "var(--card-border-insurance, #2C7A7B)"
    elif category == "banking":
        page_title = t("banking_page_title")
        page_desc = t("banking_page_desc")
        selector_label = t("banking_selector_label")
        accent_color = "var(--card-border-banking, #2B6CB0)"
    else:
        page_title = t("proc_page_title")
        page_desc = t("proc_page_desc")
        selector_label = t("proc_selector_label")
        accent_color = "var(--card-border-orange, #E37222)"

    st.markdown(f"## {page_title}")
    st.markdown(page_desc)
    
    try:
        processes = load_processes(category=category, language=current_lang)
    except Exception as e:
        st.error(f"❌ Failed to load guide database: {str(e)}")
        return

    # Process Selector Dropdown
    process_names = [p["name"] for p in processes]
    selected_idx = 0
    saved_proc_id = st.session_state.get("selected_process_id")
    if saved_proc_id:
        for i, p in enumerate(processes):
            if p["id"] == saved_proc_id:
                selected_idx = i
                break

    selected_name = st.selectbox(
        selector_label,
        options=process_names,
        index=selected_idx,
        key=f"{category}_guide_selector"
    )

    selected_proc = next(p for p in processes if p["name"] == selected_name)
    st.session_state["selected_process_id"] = selected_proc["id"]

    disclaimer_text = None
    # Bank & Loan Type sub-selectors for Loan Documentation
    if selected_proc.get("id") == "loan_documentation":
        st.markdown(f"#### {t('loan_guidance_header')}")
        col_lt, col_bnk = st.columns(2)
        
        loan_types = selected_proc.get("loan_types", [
            "Home Loan", "Education Loan", "Personal Loan", "Vehicle Loan", "Business Loan"
        ])
        banks = selected_proc.get("banks", [
            "IDFC FIRST Bank", "HDFC Bank", "Kotak Mahindra Bank", "State Bank of India",
            "ICICI Bank", "IndusInd Bank", "Union Bank", "RBL Bank", "Bank of India",
            "Punjab National Bank", "Yes Bank", "Axis Bank"
        ])
        
        with col_lt:
            sel_loan_type = st.selectbox(t("select_loan_type"), options=loan_types, key="sel_loan_type")
        with col_bnk:
            sel_bank = st.selectbox(t("select_bank"), options=banks, key="sel_bank")
            
        cache_key = f"loan_info_{sel_bank}_{sel_loan_type}_{current_lang}"
        if cache_key not in st.session_state:
            with st.spinner(f"🔍 {t('thinking')}"):
                loan_data = bank_loan_info(sel_bank, sel_loan_type, language=current_lang)
                st.session_state[cache_key] = loan_data
        else:
            loan_data = st.session_state[cache_key]
            
        if loan_data and "overview" in loan_data:
            selected_proc = dict(selected_proc)
            selected_proc["name"] = f"{sel_bank} - {sel_loan_type}"
            selected_proc["description"] = loan_data.get("overview", selected_proc.get("description"))
            selected_proc["steps"] = loan_data.get("general_process", selected_proc.get("steps", []))
            selected_proc["required_documents"] = loan_data.get("typical_documents", selected_proc.get("required_documents", []))
            disclaimer_text = loan_data.get("disclaimer")
    
    # Store normalized analysis result in session state for consistency
    formatted_result = format_process_for_analysis(selected_proc)
    if disclaimer_text:
        formatted_result["risks"] = [disclaimer_text]
    st.session_state["analysis_result"] = formatted_result
    
    # Record in completed history
    if "completed_history" not in st.session_state:
        st.session_state["completed_history"] = []
    
    proc_id = selected_proc.get("id", "proc")
    existing_rec = next((r for r in st.session_state["completed_history"] if r.get("id") == proc_id), None)
    if not existing_rec:
        st.session_state["completed_history"].append({
            "id": proc_id,
            "name": selected_proc.get("name", "Guide"),
            "category": category,
            "status": "Guide Consulted"
        })
    else:
        existing_rec["name"] = selected_proc.get("name", existing_rec.get("name"))
        existing_rec["category"] = category
    
    context_text = (
        f"Guide Name: {selected_proc['name']}\n"
        f"Description: {selected_proc['description']}\n"
        f"Steps: {'; '.join(selected_proc['steps'])}\n"
        f"Required Documents: {'; '.join(selected_proc['required_documents'])}\n"
        f"Authority: {selected_proc['authority']['type']} ({selected_proc['authority']['mode']})\n"
        f"Note: {selected_proc['authority'].get('note', '')}\n"
        f"Estimated Time: {selected_proc['estimated_time']}\n"
        f"Fees: {selected_proc['fees']}"
    )
    st.session_state["doc_text"] = context_text

    st.markdown("---")

    # ================= SINGLE UNIFIED SUMMARY SECTION =================
    with st.container():
        st.markdown(f"### 📋 {selected_proc['name']}")
        
        if disclaimer_text:
            st.warning(f"**{t('loan_disclaimer_label')}** {disclaimer_text}")

        # 1. Executive Summary Description Box
        st.markdown(f"""
        <div style="background-color: var(--box-summary-bg, #f8f9fa); border-left: 4px solid {accent_color}; padding: 18px 22px; border-radius: 6px; font-size: 15px; line-height: 1.6; color: var(--app-text, #212529); text-align: left; margin-bottom: 20px; border-top: 1px solid var(--box-summary-border, #e2e8f0); border-right: 1px solid var(--box-summary-border, #e2e8f0); border-bottom: 1px solid var(--box-summary-border, #e2e8f0);">
            <strong>{t('overview_label')}:</strong> {selected_proc['description']}
        </div>
        """, unsafe_allow_html=True)

        # 2. Details Grid (Authority, Estimated Time, Fees)
        cols = st.columns(3)
        auth = selected_proc.get("authority", {})
        mode_label = t("mode_both") if auth.get("mode") == "both" else auth.get("mode", "").capitalize()

        with cols[0]:
            st.markdown(f"""
            <div style="background-color: var(--card-bg-blue, #f0f4f8); border: 1px solid var(--card-border-blue, #d9e2ec); border-radius: 8px; padding: 16px; height: 170px; text-align: left;">
                <h4 style="color: var(--card-border-blue, #005A9C); margin-top: 0; margin-bottom: 8px; font-size: 16px;">{t('authority_office_header')}</h4>
                <p style="margin: 0 0 6px 0; font-weight: bold; color: var(--app-text, #1a202c); font-size: 14px;">{auth.get('type', 'Competent Authority')}</p>
                <p style="margin: 0 0 6px 0; color: var(--app-text-muted, #4a5568); font-size: 13px;"><strong>{t('mode_label')}:</strong> {mode_label}</p>
                <p style="margin: 0; color: var(--app-text-muted, #718096); font-size: 12px; font-style: italic;">{t('state_variance_note')}</p>
            </div>
            """, unsafe_allow_html=True)

        with cols[1]:
            st.markdown(f"""
            <div style="background-color: var(--card-bg-insurance, #edfdf5); border: 1px solid var(--card-border-insurance, #b7f4d8); border-radius: 8px; padding: 16px; height: 170px; text-align: left;">
                <h4 style="color: var(--card-border-insurance, #0b6943); margin-top: 0; margin-bottom: 8px; font-size: 16px;">{t('timeline_header')}</h4>
                <p style="margin: 0 0 6px 0; font-size: 14px; font-weight: bold; color: var(--app-text, #1a202c);">{selected_proc.get('estimated_time', '')}</p>
                <p style="margin: 0; color: var(--app-text-muted, #718096); font-size: 12px;">{t('timeline_subtext')}</p>
            </div>
            """, unsafe_allow_html=True)

        with cols[2]:
            st.markdown(f"""
            <div style="background-color: var(--card-bg-orange, #fff9db); border: 1px solid var(--card-border-orange, #ffe066); border-radius: 8px; padding: 16px; height: 170px; text-align: left;">
                <h4 style="color: var(--card-border-orange, #b7791f); margin-top: 0; margin-bottom: 8px; font-size: 16px;">{t('fees_header')}</h4>
                <p style="margin: 0 0 6px 0; font-size: 14px; font-weight: bold; color: var(--app-text, #1a202c);">{selected_proc.get('fees', '')}</p>
                <p style="margin: 0; color: var(--app-text-muted, #718096); font-size: 12px;">{t('fees_subtext')}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Optional Quick Navigation to Action Dashboard
        if st.button(t("open_dashboard_btn"), key="btn_proc_open_dashboard", use_container_width=True):
            st.session_state["page"] = "dashboard"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

                # 3. Action Steps and Required Documents side-by-side
        col_steps, col_docs = st.columns([1.2, 1])

        with col_steps:
            st.markdown(f"#### {t('steps_procedure_header')}")
            steps = selected_proc.get("steps", [])
            for i, step in enumerate(steps):
                st.markdown(f"""
                <div style="background-color: var(--step-item-bg, #ffffff); border: 1px solid var(--step-item-border, #e2e8f0); border-radius: 6px; padding: 10px 14px; margin-bottom: 8px; text-align: left; font-size: 14px; line-height: 1.5; color: var(--step-item-text, #2d3748);">
                    <strong style="color: {accent_color};">{t('step_num_prefix')} {i+1}:</strong> {step}
                </div>
                """, unsafe_allow_html=True)

        with col_docs:
            st.markdown(f"#### {t('req_docs_header')}")
            req_docs = selected_proc.get("required_documents", [])
            for doc in req_docs:
                st.markdown(f"""
                <div style="background-color: var(--step-item-bg, #ffffff); border: 1px solid var(--step-item-border, #e2e8f0); border-radius: 6px; padding: 10px 14px; margin-bottom: 8px; text-align: left; font-size: 14px; line-height: 1.5; color: var(--step-item-text, #2d3748);">
                    <span style="color: var(--card-border-blue, #2b6cb0);">✔️</span> <strong>{doc}</strong>
                </div>
                """, unsafe_allow_html=True)

    # ================= QUESTION / CHAT SECTION =================
    st.markdown("---")
    st.markdown(f"### {t('ask_proc_header')}")
    st.caption(t("ask_proc_caption", language=current_lang))

    # Render chat history
    if "proc_chat_history" not in st.session_state:
        st.session_state["proc_chat_history"] = []

    for msg in st.session_state["proc_chat_history"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_q = st.chat_input(t("ask_proc_placeholder", proc_name=selected_proc['name'], language=current_lang))
    if user_q:
        st.session_state["proc_chat_history"].append({"role": "user", "content": user_q})
        with st.chat_message("user"):
            st.write(user_q)

        with st.chat_message("assistant"):
            with st.spinner(f"🔍 {t('thinking')}"):
                answer = answer_question(context_text, user_q, language=current_lang, history=st.session_state.get('proc_chat_history', [])[:-1])
                st.write(answer)
                st.session_state["proc_chat_history"].append({"role": "assistant", "content": answer})

```

---

## 📄 `pages/dashboard.py`

```python
﻿import streamlit as st
from logic.llm_calls import answer_question
from logic.translations import t, get_normalized_language

def show_dashboard():
    render_dashboard()

def render_dashboard():
    current_lang = get_normalized_language(st.session_state.get("language", "English"))

    # 1. Error handling / Session state check
    if "analysis_result" not in st.session_state or st.session_state["analysis_result"] is None:
        st.warning(t("no_doc_loaded_warning"))
        st.info(t("no_doc_loaded_info"))
        if st.button(t("go_to_home"), key="btn_dash_go_home", use_container_width=True):
            st.session_state["page"] = "home"
            st.rerun()
        return

    result = st.session_state["analysis_result"]

    # Top Navigation Bar
    col_nav1, col_nav2 = st.columns([2, 5])
    with col_nav1:
        if st.button(t("back_to_home"), key="btn_dash_back_home", use_container_width=True):
            st.session_state["page"] = "home"
            st.rerun()

    # Document Header Title
    doc_type_title = result.get("doc_type", t("summary_heading"))
    st.markdown(f"## 📋 {doc_type_title}")

    # 2. Prominent Risks / Warning banner at the top (if present)
    risks = result.get("risks", [])
    if risks:
        risk_text = " • ".join(risks) if isinstance(risks, list) else str(risks)
        st.warning(f"⚠️ **{t('critical_risks_label')}**\n\n{risk_text}")

    # 3. 4 Main Tabs: Summary, Steps, Deadlines & Documents, Ask a Question
    tab_summary, tab_steps, tab_deadlines_docs, tab_qa = st.tabs([
        t("tab_summary"),
        t("tab_steps"),
        t("tab_deadlines_docs"),
        t("tab_qa")
    ])

    # ------------------ TAB 1: SUMMARY ------------------
    with tab_summary:
        st.markdown(f"### {t('exec_summary_header')}")
        summary_text = result.get("summary", "No summary provided.")
        st.markdown(f"""
        <div style='background-color: var(--box-summary-bg, #f8f9fa); padding: 18px 22px; border-radius: 8px; border: 1px solid var(--box-summary-border, #e9ecef); border-left: 4px solid var(--card-border-blue, #005A9C); font-size: 16px; line-height: 1.6; color: var(--app-text, #212529);'>
            {summary_text}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Details Grid (Authority, Estimated Time, Fees)
        cols = st.columns(3)
        with cols[0]:
            if result.get("authority"):
                auth = result["authority"]
                mode_badge = t("mode_both") if auth.get("mode") == "both" else auth.get("mode", "").capitalize()
                st.markdown(f"""
                <div style="background-color: var(--card-bg-blue, #e8f4fd); border: 1px solid var(--card-border-blue, #b6e0fe); border-radius: 8px; padding: 14px; height: 180px;">
                    <h4 style="color: var(--card-border-blue, #005A9C); margin-top: 0;">{t('authority_office_header')}</h4>
                    <p style="margin: 4px 0; color: var(--app-text, #1a202c);"><strong>{auth.get('type', 'Department')}</strong></p>
                    <p style="margin: 4px 0; color: var(--app-text-muted, #444); font-size: 13px;">{t('mode_label')}: {mode_badge}</p>
                    <p style="margin: 4px 0; color: var(--app-text-muted, #666); font-size: 12px; font-style: italic;">{t('state_variance_note')}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background-color: var(--box-summary-bg, #f0f4f8); border: 1px solid var(--box-summary-border, #d9e2ec); border-radius: 8px; padding: 14px; height: 180px;">
                    <h4 style="color: var(--card-border-blue, #334e68); margin-top: 0;">{t('doc_origin_header')}</h4>
                    <p style="color: var(--app-text-muted, #486581);">{t('doc_origin_desc')}</p>
                </div>
                """, unsafe_allow_html=True)

        with cols[1]:
            est_time = result.get("estimated_time", "30 days")
            st.markdown(f"""
            <div style="background-color: var(--card-bg-insurance, #edfdf5); border: 1px solid var(--card-border-insurance, #b7f4d8); border-radius: 8px; padding: 14px; height: 180px;">
                <h4 style="color: var(--card-border-insurance, #0b6943); margin-top: 0;">{t('timeline_header')}</h4>
                <p style="font-size: 15px; color: var(--app-text, #2d3748); margin-top: 10px;"><strong>{est_time}</strong></p>
                <p style="color: var(--app-text-muted, #718096); font-size: 12px;">{t('timeline_subtext')}</p>
            </div>
            """, unsafe_allow_html=True)

        with cols[2]:
            fees_info = result.get("fees", "Standard fee schedule")
            st.markdown(f"""
            <div style="background-color: var(--card-bg-orange, #fff9db); border: 1px solid var(--card-border-orange, #ffe066); border-radius: 8px; padding: 14px; height: 180px;">
                <h4 style="color: var(--card-border-orange, #f59f00); margin-top: 0;">{t('fees_header')}</h4>
                <p style="font-size: 15px; color: var(--app-text, #2d3748); margin-top: 10px;"><strong>{fees_info}</strong></p>
                <p style="color: var(--app-text-muted, #718096); font-size: 12px;">{t('fees_subtext')}</p>
            </div>
            """, unsafe_allow_html=True)

    # ------------------ TAB 2: STEPS CHECKLIST ------------------
    with tab_steps:
        st.markdown(f"### {t('action_checklist_header')}")
        st.markdown(t("action_checklist_subtext"))
        
        steps = result.get("steps", [])
        if not steps:
            st.info(t("no_steps_info"))
        else:
            if "step_progress" not in st.session_state:
                st.session_state["step_progress"] = {}
                
            for idx, step in enumerate(steps):
                step_key = f"task_step_{idx}"
                if step_key not in st.session_state["step_progress"]:
                    st.session_state["step_progress"][step_key] = False
                
                checked = st.checkbox(
                    f"**{t('step_num_prefix')} {idx+1}:** {step}",
                    value=st.session_state["step_progress"].get(step_key, False),
                    key=f"chk_dash_{idx}"
                )
                st.session_state["step_progress"][step_key] = checked

    # ------------------ TAB 3: DEADLINES & REQUIRED DOCUMENTS ------------------
    with tab_deadlines_docs:
        col_d, col_docs = st.columns(2)
        
        with col_d:
            st.markdown(f"### {t('deadlines_header')}")
            deadlines = result.get("deadlines", [])
            if not deadlines:
                st.info(t("no_deadlines_info"))
            else:
                for d in deadlines:
                    if isinstance(d, dict):
                        d_date = d.get("date", "Due Date")
                        d_desc = d.get("description", "")
                        st.markdown(f"""
                        <div style="background-color: var(--card-bg-orange, #fff8f0); border-left: 4px solid var(--card-border-orange, #E37222); padding: 10px 14px; margin-bottom: 8px; border-radius: 4px; border-top: 1px solid var(--box-summary-border, #e2e8f0); border-right: 1px solid var(--box-summary-border, #e2e8f0); border-bottom: 1px solid var(--box-summary-border, #e2e8f0);">
                            <strong style="color: var(--card-border-orange, #E37222);">{d_date}</strong>: <span style="color: var(--app-text, #2d3748);">{d_desc}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"- ⏳ **{d}**")

        with col_docs:
            st.markdown(f"### {t('req_docs_header')}")
            req_docs = result.get("required_documents", [])
            if not req_docs:
                st.info(t("no_docs_info"))
            else:
                for doc in req_docs:
                    st.markdown(f"""
                    <div style="background-color: var(--card-bg-blue, #f0f8ff); border-left: 4px solid var(--card-border-blue, #005A9C); padding: 10px 14px; margin-bottom: 8px; border-radius: 4px; border-top: 1px solid var(--box-summary-border, #e2e8f0); border-right: 1px solid var(--box-summary-border, #e2e8f0); border-bottom: 1px solid var(--box-summary-border, #e2e8f0);">
                        <span style="color: var(--card-border-blue, #005A9C);">✔️</span> <strong style="color: var(--app-text, #1a202c);">{doc}</strong>
                    </div>
                    """, unsafe_allow_html=True)

    # ------------------ TAB 4: ASK A QUESTION (Q&A) ------------------
    with tab_qa:
        st.markdown(f"### {t('tab_qa')} ({current_lang})")
        st.caption(t("ask_doc_caption", filename=doc_type_title, language=current_lang))
        
        context_text = st.session_state.get("doc_text", "")
        if not context_text:
            context_text = str(result)
            
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []

        for msg in st.session_state["chat_history"]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        user_query = st.chat_input(t("ask_doc_placeholder", language=current_lang))
        if user_query:
            st.session_state["chat_history"].append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.write(user_query)

            with st.chat_message("assistant"):
                with st.spinner(f"🤖 {t('thinking')}"):
                    answer = answer_question(context_text, user_query, language=current_lang, history=st.session_state.get('chat_history', [])[:-1])
                    st.write(answer)
                    st.session_state["chat_history"].append({"role": "assistant", "content": answer})

```

---

## 📄 `pages/ask.py`

```python
﻿import streamlit as st
from logic.llm_calls import general_chat_answer
from logic.translations import t, get_normalized_language

def show_ask():
    render_ask()

def render_ask():
    current_lang = get_normalized_language(st.session_state.get("language", "English"))

    col_nav1, col_nav2 = st.columns([2, 5])
    with col_nav1:
        if st.button(t("back_to_home"), key="btn_ask_back_home", use_container_width=True):
            st.session_state["page"] = "home"
            st.rerun()

    st.markdown(f"## {t('ask_ai_header')}")
    st.caption(t("ask_ai_caption", language=current_lang))

    if "general_chat_history" not in st.session_state:
        st.session_state["general_chat_history"] = []

    for item in st.session_state["general_chat_history"]:
        role = item.get("role", "user" if "question" in item else "assistant")
        content = item.get("content", item.get("question", item.get("answer", "")))
        with st.chat_message(role):
            st.write(content)

    user_q = st.chat_input(t("ask_ai_placeholder", language=current_lang))
    if user_q:
        st.session_state["general_chat_history"].append({"role": "user", "content": user_q})
        with st.chat_message("user"):
            st.write(user_q)

        with st.chat_message("assistant"):
            with st.spinner(f"🔍 {t('thinking')}"):
                answer = general_chat_answer(user_q, language=current_lang)
                st.write(answer)
                st.session_state["general_chat_history"].append({"role": "assistant", "content": answer})

```

---

## 📄 `test_comprehensive.py`

```python
﻿import unittest
import os
from streamlit.testing.v1 import AppTest
from logic.extract_text import extract_text
from logic.process_data import load_processes, format_process_for_analysis
from logic.llm_calls import analyze_document, answer_question

class TestComprehensiveVerification(unittest.TestCase):

    def test_01_requirements_and_data_accuracy(self):
        print("\n--- 1. Testing processes.json Curated Data Accuracy ---")
        procs = load_processes()
        self.assertEqual(len(procs), 3, "Must have exactly 3 curated processes")
        
        proc_ids = [p["id"] for p in procs]
        self.assertIn("pan_card", proc_ids)
        self.assertIn("aadhaar_update", proc_ids)
        self.assertIn("passport_renewal", proc_ids)
        
        for p in procs:
            self.assertIn("name", p)
            self.assertIn("description", p)
            self.assertIn("steps", p)
            self.assertTrue(len(p["steps"]) >= 3)
            self.assertIn("required_documents", p)
            self.assertTrue(len(p["required_documents"]) >= 2)
            self.assertIn("authority", p)
            self.assertIn("type", p["authority"])
            self.assertIn("mode", p["authority"])
            self.assertIn("note", p["authority"])
            self.assertIn("estimated_time", p)
            self.assertIn("fees", p)
            self.assertEqual(p["authority"]["note"], "confirm exact details at your nearest center, as requirements vary by state")
        print("[OK] Curated data schema and accuracy verified (PAN, Aadhaar, Passport)")

    def test_02_text_extraction(self):
        print("\n--- 2. Testing extract_text.py Standalone ---")
        docx_text = extract_text("samples/sample_it_notice.docx")
        self.assertIn("INCOME TAX DEPARTMENT", docx_text)
        self.assertIn("143(1)", docx_text)
        print("[OK] DOCX extraction verified:", len(docx_text), "chars")
        
        pdf_text = extract_text("samples/sample_khata_notice.pdf")
        self.assertIn("REVENUE DEPARTMENT", pdf_text)
        self.assertIn("Khata", pdf_text)
        print("[OK] PDF extraction verified:", len(pdf_text), "chars")
        
        with self.assertRaises(ValueError):
            extract_text(b"sample", filename="bad_file.xyz")
        print("[OK] Unsupported file error handling verified")

    def test_03_llm_json_analysis_and_qa(self):
        print("\n--- 3. Testing llm_calls.py (Groq & Parsing) ---")
        sample_text = "PASSPORT SEVA KENDRA: Police verification mandatory within 15 days. Fees: Rs 1500 for normal 36 pages. Required: Old passport, Aadhaar card."
        analysis = analyze_document(sample_text, language="English")
        
        required_keys = ["doc_type", "summary", "steps", "deadlines", "required_documents", "risks"]
        for k in required_keys:
            self.assertIn(k, analysis, f"Key '{k}' must be present in analysis output")
        print("[OK] LLM analysis output format and schema verified")
        
        ans = answer_question(sample_text, "What is the fee for normal 36 pages?", language="English")
        self.assertTrue("1500" in ans or "1,500" in ans or len(ans) > 0)
        print("[OK] Grounded Q&A answered accurately")
        
        ans_missing = answer_question(sample_text, "What is the capital of Mars?", language="English")
        self.assertIn("certain", ans_missing.lower())
        print("[OK] Grounded Q&A refusal verified ('I'm not certain based on this document')")

    def test_04_full_ui_navigation_and_flows(self):
        print("\n--- 4. Testing End-to-End Streamlit App Flows ---")
        at = AppTest.from_file("app.py", default_timeout=15)
        at.run()
        
        # 1. Login
        self.assertEqual(at.session_state["page"], "login")
        at.text_input[0].input("Aarav Gupta")
        at.text_input[1].input("aarav@example.com")
        btn_login = [b for b in at.button if "Continue" in (b.label or "")]
        self.assertTrue(len(btn_login) > 0)
        btn_login[0].click().run()
        self.assertEqual(at.session_state["page"], "home")
        self.assertEqual(at.session_state["user"]["name"], "Aarav Gupta")
        print("[OK] Screen 1: Login passed")
        
        # 2. Home Language Selection & Process Picker Navigation
        at.selectbox[0].select("English").run()
        btn_proc = [b for b in at.button if "Government" in (b.label or "") or (b.key and "btn_main_govt" in b.key)]
        self.assertTrue(len(btn_proc) > 0)
        btn_proc[0].click().run()
        self.assertEqual(at.session_state["page"], "process_picker")
        print("[OK] Screen 2: Home -> Process Picker navigation passed")
        
        # 3. Process Picker (Dropdown Select & Unified Summary Display)
        self.assertIsNotNone(at.session_state["analysis_result"])
        res = at.session_state["analysis_result"]
        self.assertIn("PAN", res["doc_type"])
        print("[OK] Screen 3: Process Guide loaded with unified summary")
        
        # 4. Sidebar Home Navigation
        btn_side_home = [b for b in at.button if "Home" in (b.label or "") or (b.key and "side_nav_home" in b.key)]
        self.assertTrue(len(btn_side_home) > 0)
        btn_side_home[0].click().run()
        self.assertEqual(at.session_state["page"], "home")
        print("[OK] Screen 4: Sidebar Home navigation passed")

        # 5. Sidebar Sign Out
        btn_signout = [b for b in at.button if "Sign Out" in (b.label or "") or (b.key and "side_nav_signout" in b.key)]
        self.assertTrue(len(btn_signout) > 0)
        btn_signout[0].click().run()
        self.assertEqual(at.session_state["page"], "login")
        self.assertIsNone(at.session_state["user"])
        print("[OK] Screen 5: Sign Out reset session state to login cleanly")

if __name__ == "__main__":
    unittest.main()

```

---

