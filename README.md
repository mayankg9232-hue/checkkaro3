# 🇮🇳 CheckKaro — Multilingual Document & Indian Process Assistant

CheckKaro is an intelligent, multilingual AI assistant designed to simplify complex Indian legal, administrative, government notices, banking workflows, and insurance processes into clear, actionable steps in regional languages (English, Hindi, Kannada, Tamil, Telugu, Marathi, Gujarati, Bengali, and more).

---

## ✨ Features

- 📄 **Multi-Format Document Analysis**: Upload PDF or DOCX notices, letters, or policies for instant parsing and structured breakdown.
- 🌐 **Multilingual Plain-Language Summaries**: Translates dense legal jargon into easy-to-understand explanations in multiple Indian regional languages.
- ⚡ **Actionable Checklists & Deadlines**: Identifies critical dates, penalty warnings, required paperwork, and step-by-step procedures.
- 🏦 **Comprehensive Domain Support**:
  - **Government & Civic**: Income Tax Notices (143(1)), Khata Transfer, Driving License, Passport, PAN/Aadhaar corrections, Property Registration.
  - **Banking & Finance**: Home Loans, Personal Loans, KYC updates, Chargeback claims, Account settlements.
  - **Insurance**: Health Claims, Motor Insurance claim processes, Term Life documentation.
- 💬 **Interactive Document Q&A**: Real-time context-aware chat assistant for any uploaded notice or policy.

---

## 🏗️ Architecture

```
doc_assistant/
├── app.py                      # Main Streamlit application entrypoint & state manager
├── logic/
│   ├── extract_text.py         # Robust text extraction for PDF and DOCX
│   ├── llm_calls.py            # Groq / LLM orchestration & JSON formatting
│   ├── process_data.py         # Knowledge engine & process metadata matching
│   └── translations.py         # Multilingual UI localization dictionary
├── pages/
│   ├── home.py                 # Landing page & quick category launcher
│   ├── upload.py               # Document upload and file inspection
│   ├── process_picker.py       # Domain-specific process navigator
│   ├── dashboard.py            # Analysis results, deadlines, risks & steps view
│   ├── ask.py                  # Interactive document Q&A assistant
│   └── login.py                # User authentication & session init
├── data/
│   ├── processes.json          # Government & civic process templates
│   ├── banking_processes.json  # Banking workflow definitions
│   └── insurance_processes.json# Insurance claim & policy procedures
└── samples/                    # Sample test notices (PDF, DOCX)
```

---

## 🚀 Quickstart

### 1. Prerequisites
- Python 3.9+
- Git

### 2. Installation

Clone the repository and install dependencies:
```bash
git clone git@github.com:mayankg9232-hue/checkkaro3.git
cd checkkaro3
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env` and add your API key:
```bash
cp .env.example .env
```
Edit `.env`:
```ini
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Run Application
```bash
streamlit run app.py
```

---

## 🧪 Testing

Run test suites to verify extraction, LLM parsing, and multilingual flows:
```bash
python -m unittest discover -s . -p "test_*.py"
```