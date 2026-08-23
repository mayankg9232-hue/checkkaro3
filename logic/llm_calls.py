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
