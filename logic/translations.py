import streamlit as st
import string

TRANSLATIONS = {
    # ------------------ Navigation & Global ------------------
    "app_title": {
        "English": "Document & Process Assistant",
        "Hindi": "दस्तावेज़ एवं प्रक्रिया सहायक",
        "Kannada": "ದಾಖಲೆ ಮತ್ತು ಪ್ರಕ್ರಿಯಾ ಸಹಾಯಕ"
    },
    "language": {
        "English": "🌐 Language",
        "Hindi": "🌐 भाषा (Language)",
        "Kannada": "🌐 ಭಾಷೆ (Language)"
    },
    "quick_navigation": {
        "English": "🧭 Quick Navigation",
        "Hindi": "🧭 त्वरित नेविगेशन",
        "Kannada": "🧭 ತ್ವರಿತ ನ್ಯಾವಿಗೇಷನ್"
    },
    "home": {
        "English": "🏠 Home",
        "Hindi": "🏠 होम",
        "Kannada": "🏠 ಮುಖಪುಟ"
    },
    "current_task": {
        "English": "📋 Current Task",
        "Hindi": "📋 वर्तमान कार्य",
        "Kannada": "📋 ಪ್ರಸ್ತುತ ಕಾರ್ಯ"
    },
    "completed_task": {
        "English": "✅ Completed Task",
        "Hindi": "✅ पूर्ण कार्य",
        "Kannada": "✅ ಪೂರ್ಣಗೊಂಡ ಕಾರ್ಯ"
    },
    "sign_out": {
        "English": "🚪 Sign Out",
        "Hindi": "🚪 साइन आउट",
        "Kannada": "🚪 ಸೈನ್ ಔಟ್"
    },
    "back_to_home": {
        "English": "← Back to Home",
        "Hindi": "← होम पर वापस जाएं",
        "Kannada": "← ಮುಖಪುಟಕ್ಕೆ ಹಿಂತಿರುಗಿ"
    },
    "go_to_home": {
        "English": "← Go to Home",
        "Hindi": "← होम पर जाएं",
        "Kannada": "← ಮುಖಪುಟಕ್ಕೆ ಹೋಗಿ"
    },
    "thinking": {
        "English": "Thinking...",
        "Hindi": "विचार कर रहा हूँ...",
        "Kannada": "ಯೋಚಿಸುತ್ತಿದೆ..."
    },
    "loading": {
        "English": "Loading...",
        "Hindi": "लोड हो रहा है...",
        "Kannada": "ಲೋಡ್ ಆಗುತ್ತಿದೆ..."
    },

    # ------------------ Login Screen ------------------
    "hero_title": {
        "English": "🇮🇳 Multilingual Document & Process Assistant",
        "Hindi": "🇮🇳 बहुभाषी दस्तावेज़ एवं प्रक्रिया सहायक",
        "Kannada": "🇮🇳 ಬಹುಭಾಷಾ ದಾಖಲೆ ಮತ್ತು ಪ್ರಕ್ರಿಯಾ ಸಹಾಯಕ"
    },
    "hero_subtitle": {
        "English": "Simplifying official notices, legal documents, and Indian citizen procedures in English, Hindi, and Kannada.",
        "Hindi": "अंग्रेजी, हिंदी और कन्नड़ में आधिकारिक नोटिस, कानूनी दस्तावेजों और भारतीय नागरिक प्रक्रियाओं को सरल बनाना।",
        "Kannada": "ಇಂಗ್ಲಿಷ್, ಹಿಂದಿ ಮತ್ತು ಕನ್ನಡದಲ್ಲಿ ಅಧಿಕೃತ ಸೂಚನೆಗಳು, ಕಾನೂನು ದಾಖಲೆಗಳು ಮತ್ತು ಭಾರತೀಯ ನಾಗರಿಕ ಪ್ರಕ್ರಿಯೆಗಳನ್ನು ಸರಳಗೊಳಿಸುವುದು."
    },
    "sign_in_title": {
        "English": "Sign In to Begin",
        "Hindi": "शुरू करने के लिए साइन इन करें",
        "Kannada": "ಪ್ರಾರಂಭಿಸಲು ಸೈನ್ ಇನ್ ಮಾಡಿ"
    },
    "sign_in_subtitle": {
        "English": "Enter your details to access document breakdown and government guides.",
        "Hindi": "दस्तावेज़ विश्लेषण और सरकारी गाइड तक पहुँचने के लिए अपना विवरण दर्ज करें।",
        "Kannada": "ದಾಖಲೆ ವಿಶ್ಲೇಷಣೆ ಮತ್ತು ಸರ್ಕಾರಿ ಮಾರ್ಗದರ್ಶಿಗಳನ್ನು ಪ್ರವೇಶಿಸಲು ನಿಮ್ಮ ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ."
    },
    "full_name_label": {
        "English": "Full Name *",
        "Hindi": "पूरा नाम *",
        "Kannada": "ಪೂರ್ಣ ಹೆಸರು *"
    },
    "full_name_placeholder": {
        "English": "e.g. Ramesh Kumar / Priya Sharma",
        "Hindi": "उदा. रमेश कुमार / प्रिया शर्मा",
        "Kannada": "ಉದಾ. ರಮೇಶ್ ಕುಮಾರ್ / ಪ್ರಿಯಾ ಶರ್ಮಾ"
    },
    "email_label": {
        "English": "Email Address (Optional)",
        "Hindi": "ईमेल पता (वैकल्पिक)",
        "Kannada": "ಇಮೇಲ್ ವಿಳಾಸ (ಐಚ್ಛಿಕ)"
    },
    "email_placeholder": {
        "English": "e.g. ramesh@example.com",
        "Hindi": "उदा. ramesh@example.com",
        "Kannada": "ಉದಾ. ramesh@example.com"
    },
    "continue_btn": {
        "English": "Continue to Assistant ➔",
        "Hindi": "सहायक पर जारी रखें ➔",
        "Kannada": "ಸಹಾಯಕಕ್ಕೆ ಮುಂದುವರಿಯಿರಿ ➔"
    },
    "name_required_warning": {
        "English": "⚠️ Please provide your name to continue.",
        "Hindi": "⚠️ जारी रखने के लिए कृपया अपना नाम दर्ज करें।",
        "Kannada": "⚠️ ಮುಂದುವರಿಯಲು ದಯವಿಟ್ಟು ನಿಮ್ಮ ಹೆಸರನ್ನು ನಮೂದಿಸಿ."
    },
    "badge_notice": {
        "English": "📑 <strong>Notice Explainer</strong><br>ITR, Courts, Utilities",
        "Hindi": "📑 <strong>नोटिस व्याख्याकार</strong><br>आईटीआर, न्यायालय, उपयोगिताएं",
        "Kannada": "📑 <strong>ಸೂಚನೆ ವಿವರಣೆಗಾರ</strong><br>ಐಟಿಆರ್, ನ್ಯಾಯಾಲಯಗಳು"
    },
    "badge_govt": {
        "English": "🏛️ <strong>3 Core Govt Services</strong><br>PAN, Aadhaar, Passport",
        "Hindi": "🏛️ <strong>3 प्रमुख सरकारी सेवाएं</strong><br>पैन, आधार, पासपोर्ट",
        "Kannada": "🏛️ <strong>3 ಪ್ರಮುಖ ಸರ್ಕಾರಿ ಸೇವೆಗಳು</strong><br>ಪ್ಯಾನ್, ಆಧಾರ್, ಪಾಸ್‌ಪೋರ್ಟ್"
    },
    "badge_multi": {
        "English": "🌐 <strong>Multilingual</strong><br>English, हिन्दी, ಕನ್ನಡ",
        "Hindi": "🌐 <strong>बहुभाषी</strong><br>English, हिन्दी, ಕನ್ನಡ",
        "Kannada": "🌐 <strong>ಬಹುಭಾಷಾ</strong><br>English, हिन्दी, ಕನ್ನಡ"
    },

    # ------------------ Home Screen ------------------
    "welcome_greeting": {
        "English": "Welcome, {user_name}! 👋",
        "Hindi": "नमस्ते, {user_name}! 🙏",
        "Kannada": "ಸ್ವಾಗತ, {user_name}! 🙏"
    },
    "site_description": {
        "English": "Your step-by-step guide through documents and government processes.",
        "Hindi": "दस्तावेजों और सरकारी प्रक्रियाओं के लिए आपका चरण-दर-चरण मार्गदर्शक।",
        "Kannada": "ದಾಖಲೆಗಳು ಮತ್ತು ಸರ್ಕಾರಿ ಪ್ರಕ್ರಿಯೆಗಳ ಮೂಲಕ ನಿಮ್ಮ ಹಂತ-ಹಂತದ ಮಾರ್ಗದರ್ಶಿ."
    },
    "upload_banner_title": {
        "English": "📄 Upload Document for AI Breakdown & Q&A",
        "Hindi": "📄 एआई विश्लेषण और प्रश्नोत्तर के लिए दस्तावेज़ अपलोड करें",
        "Kannada": "📄 ಎಐ ವಿಶ್ಲೇಷಣೆ ಮತ್ತು ಪ್ರಶ್ನೋತ್ತರಕ್ಕಾಗಿ ದಾಖಲೆಯನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ"
    },
    "upload_banner_desc": {
        "English": "Upload any official letter, tax notice, bill, or government form (PDF / DOCX) to get a clear breakdown in your language.",
        "Hindi": "अपनी भाषा में स्पष्ट विश्लेषण प्राप्त करने के लिए कोई भी आधिकारिक पत्र, कर नोटिस, बिल या सरकारी फॉर्म (PDF / DOCX) अपलोड करें।",
        "Kannada": "ನಿಮ್ಮ ಭಾಷೆಯಲ್ಲಿ ಸ್ಪಷ್ಟ ವಿಶ್ಲೇಷಣೆಯನ್ನು ಪಡೆಯಲು ಯಾವುದೇ ಅಧಿಕೃತ ಪತ್ರ, ತೆರಿಗೆ ಸೂಚನೆ, ಬಿಲ್ ಅಥವಾ ಸರ್ಕಾರಿ ಫಾರ್ಮ್ (PDF / DOCX) ಅನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ."
    },
    "upload_analyze_btn": {
        "English": "🚀 Upload & Analyze Document ➔",
        "Hindi": "🚀 दस्तावेज़ अपलोड और विश्लेषण करें ➔",
        "Kannada": "🚀 ದಾಖಲೆ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ಮತ್ತು ವಿಶ್ಲೇಷಿಸಿ ➔"
    },
    "ask_ai_header": {
        "English": "💬 Ask AI Assistant (General Questions & Process Help)",
        "Hindi": "💬 एआई सहायक से पूछें (सामान्य प्रश्न और प्रक्रिया सहायता)",
        "Kannada": "💬 ಎಐ ಸಹಾಯಕನನ್ನು ಕೇಳಿ (ಸಾಮಾನ್ಯ ಪ್ರಶ್ನೆಗಳು ಮತ್ತು ಪ್ರಕ್ರಿಯಾ ಸಹಾಯ)"
    },
    "ask_ai_caption": {
        "English": "Ask any question about Indian citizen services, PAN, Aadhaar, Passport, tax notices, bank KYC, or legal terms in **{language}**.",
        "Hindi": "**{language}** में भारतीय नागरिक सेवाओं, पैन, आधार, पासपोर्ट, कर नोटिस, बैंक केवाईसी या कानूनी शर्तों के बारे में कोई भी प्रश्न पूछें।",
        "Kannada": "**{language}** ನಲ್ಲಿ ಭಾರತೀಯ ನಾಗರಿಕ ಸೇವೆಗಳು, ಪ್ಯಾನ್, ಆಧಾರ್, ಪಾಸ್‌ಪೋರ್ಟ್, ತೆರಿಗೆ ಸೂಚನೆಗಳು, ಬ್ಯಾಂಕ್ ಕೆವೈಸಿ ಅಥವಾ ಕಾನೂನು ನಿಯಮಗಳ ಬಗ್ಗೆ ಯಾವುದೇ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ."
    },
    "ask_ai_placeholder": {
        "English": "Ask any question in {language} (e.g. How do I link Aadhaar with PAN?)...",
        "Hindi": "{language} में कोई भी प्रश्न पूछें (उदा. आधार को पैन से कैसे लिंक करें?)...",
        "Kannada": "{language} ನಲ್ಲಿ ಯಾವುದೇ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ (ಉದಾ. ಆಧಾರ್ ಅನ್ನು ಪ್ಯಾನ್‌ನೊಂದಿಗೆ ಲಿಂಕ್ ಮಾಡುವುದು ಹೇಗೆ?)..."
    },
    "services_header": {
        "English": "🏛️ Process Guides & Citizen Services",
        "Hindi": "🏛️ प्रक्रिया मार्गदर्शिका और नागरिक सेवाएं",
        "Kannada": "🏛️ ಪ್ರಕ್ರಿಯಾ ಮಾರ್ಗದರ್ಶಿಗಳು ಮತ್ತು ನಾಗರಿಕ ಸೇವೆಗಳು"
    },
    "card_govt_title": {
        "English": "🏛️ Government Services",
        "Hindi": "🏛️ सरकारी सेवाएं",
        "Kannada": "🏛️ ಸರ್ಕಾರಿ ಸೇವೆಗಳು"
    },
    "card_govt_desc": {
        "English": "Step-by-step guidance, required documents, fees, and authority details for PAN, Aadhaar, and Passport.",
        "Hindi": "पैन, आधार और पासपोर्ट के लिए चरण-दर-चरण मार्गदर्शन, आवश्यक दस्तावेज, शुल्क और प्राधिकरण विवरण।",
        "Kannada": "ಪ್ಯಾನ್, ಆಧಾರ್ ಮತ್ತು ಪಾಸ್‌ಪೋರ್ಟ್‌ಗಾಗಿ ಹಂತ-ಹಂತದ ಮಾರ್ಗದರ್ಶನ, ಅಗತ್ಯ ದಾಖಲೆಗಳು, ಶುಲ್ಕಗಳು ಮತ್ತು ಪ್ರಾಧಿಕಾರದ ವಿವರಗಳು."
    },
    "card_govt_badge": {
        "English": "No upload needed • Official procedures",
        "Hindi": "अपलोड की आवश्यकता नहीं • आधिकारिक प्रक्रियाएं",
        "Kannada": "ಅಪ್‌ಲೋಡ್ ಅಗತ್ಯವಿಲ್ಲ • ಅಧಿಕೃತ ಕಾರ್ಯವಿಧಾನಗಳು"
    },
    "card_govt_btn": {
        "English": "Explore Government Services ➔",
        "Hindi": "सरकारी सेवाएं देखें ➔",
        "Kannada": "ಸರ್ಕಾರಿ ಸೇವೆಗಳನ್ನು ಅನ್ವೇಷಿಸಿ ➔"
    },
    "card_banking_title": {
        "English": "🏦 Banking Services",
        "Hindi": "🏦 बैंकिंग सेवाएं",
        "Kannada": "🏦 ಬ್ಯಾಂಕಿಂಗ್ ಸೇವೆಗಳು"
    },
    "card_banking_desc": {
        "English": "Guidance for bank account transfers, re-KYC updates, loan documentation, and fixed deposit claims.",
        "Hindi": "बैंक खाता स्थानांतरण, पुनः केवाईसी अपडेट, ऋण दस्तावेज और सावधि जमा दावों के लिए मार्गदर्शन।",
        "Kannada": "ಬ್ಯಾಂಕ್ ಖಾತೆ ವರ್ಗಾವಣೆಗಳು, ಮರು-ಕೆವೈಸಿ ಅಪ್‌ಡೇಟ್‌ಗಳು, ಸಾಲದ ದಾಖಲಾತಿ ಮತ್ತು ಠೇವಣಿ ಕ್ಲೈಮ್‌ಗಳ ಮಾರ್ಗದರ್ಶನ."
    },
    "card_banking_badge": {
        "English": "Financial checklists • Branch procedures",
        "Hindi": "वित्तीय चेकलिस्ट • शाखा प्रक्रियाएं",
        "Kannada": "ಹಣಕಾಸಿನ ಪರಿಶೀಲನಾಪಟ್ಟಿಗಳು • ಶಾಖೆಯ ಕಾರ್ಯವಿಧಾನಗಳು"
    },
    "card_banking_btn": {
        "English": "Explore Banking Services ➔",
        "Hindi": "बैंकिंग सेवाएं देखें ➔",
        "Kannada": "ಬ್ಯಾಂಕಿಂಗ್ ಸೇವೆಗಳನ್ನು ಅನ್ವೇಷಿಸಿ ➔"
    },
    "card_insurance_title": {
        "English": "🛡️ Insurance Services",
        "Hindi": "🛡️ बीमा सेवाएं",
        "Kannada": "🛡️ ವಿಮಾ ಸೇವೆಗಳು"
    },
    "card_insurance_desc": {
        "English": "Step-by-step guidance for health, life, and auto insurance claims, policy terms, and required forms.",
        "Hindi": "स्वास्थ्य, जीवन और ऑटो बीमा दावों, पॉलिसी शर्तों और आवश्यक फॉर्मों के लिए चरण-दर-चरण मार्गदर्शन।",
        "Kannada": "ಆರೋಗ್ಯ, ಜೀವ ಮತ್ತು ವಾಹನ ವಿಮಾ ಕ್ಲೈಮ್‌ಗಳು, ಪಾಲಿಸಿ ನಿಯಮಗಳು ಮತ್ತು ಅಗತ್ಯ ನಮೂನೆಗಳ ಹಂತ-ಹಂತದ ಮಾರ್ಗದರ್ಶನ."
    },
    "card_insurance_badge": {
        "English": "Claim filing guides • Document checklist",
        "Hindi": "दावा दायर करने की गाइड • दस्तावेज़ चेकलिस्ट",
        "Kannada": "ಕ್ಲೈಮ್ ಸಲ್ಲಿಕೆ ಮಾರ್ಗದರ್ಶಿಗಳು • ದಾಖಲೆಗಳ ಪರಿಶೀಲನಾಪಟ್ಟಿ"
    },
    "card_insurance_btn": {
        "English": "Explore Insurance Services ➔",
        "Hindi": "बीमा सेवाएं देखें ➔",
        "Kannada": "ವಿಮಾ ಸೇವೆಗಳನ್ನು ಅನ್ವೇಷಿಸಿ ➔"
    },
    "notice_banking_coming": {
        "English": "🏦 **Banking Services Guide** is coming soon! (Loan documentation, KYC, Account Transfer guides)",
        "Hindi": "🏦 **बैंकिंग सेवा गाइड** जल्द आ रही है! (ऋण दस्तावेज, केवाईसी, खाता स्थानांतरण गाइड)",
        "Kannada": "🏦 **ಬ್ಯಾಂಕಿಂಗ್ ಸೇವಾ ಮಾರ್ಗದರ್ಶಿ** ಶೀಘ್ರದಲ್ಲೇ ಬರಲಿದೆ! (ಸಾಲದ ದಾಖಲಾತಿ, ಕೆವೈಸಿ, ಖಾತೆ ವರ್ಗಾವಣೆ ಮಾರ್ಗದರ್ಶಿಗಳು)"
    },
    "notice_insurance_coming": {
        "English": "🛡️ **Insurance Guide** is coming soon! (Claim filing, Policy breakdown, Health/Auto coverage)",
        "Hindi": "🛡️ **बीमा गाइड** जल्द आ रही है! (दावा दाखिल करना, पॉलिसी विवरण, स्वास्थ्य/वाहन कवरेज)",
        "Kannada": "🛡️ **ವಿಮಾ ಮಾರ್ಗದರ್ಶಿ** ಶೀಘ್ರದಲ್ಲೇ ಬರಲಿದೆ! (ಕ್ಲೈಮ್ ಸಲ್ಲಿಕೆ, ಪಾಲಿಸಿ ವಿವರಣೆ, ಆರೋಗ್ಯ/ವಾಹನ ರಕ್ಷಣೆ)"
    },

    # ------------------ Upload Screen ------------------
    "upload_page_title": {
        "English": "📄 Upload & Analyze Document",
        "Hindi": "📄 दस्तावेज़ अपलोड और विश्लेषण",
        "Kannada": "📄 ದಾಖಲೆ ಅಪ್‌ಲೋಡ್ ಮತ್ತು ವಿಶ್ಲೇಷಣೆ"
    },
    "upload_file_prompt": {
        "English": "Select a PDF or DOCX file to analyze:",
        "Hindi": "विश्लेषण के लिए एक PDF या DOCX फ़ाइल चुनें:",
        "Kannada": "ವಿಶ್ಲೇಷಿಸಲು PDF ಅಥವಾ DOCX ಫೈಲ್ ಆಯ್ಕೆಮಾಡಿ:"
    },
    "upload_empty_info": {
        "English": "💡 Please choose a document (PDF or DOCX) to begin analysis.",
        "Hindi": "💡 विश्लेषण शुरू करने के लिए कृपया एक दस्तावेज़ (PDF या DOCX) चुनें।",
        "Kannada": "💡 ವಿಶ್ಲೇಷಣೆ ಪ್ರಾರಂಭಿಸಲು ದಯವಿಟ್ಟು ದಾಖಲೆಯನ್ನು (PDF ಅಥವಾ DOCX) ಆಯ್ಕೆಮಾಡಿ."
    },
    "file_name_label": {
        "English": "File Name",
        "Hindi": "फ़ाइल का नाम",
        "Kannada": "ಫೈಲ್ ಹೆಸರು"
    },
    "file_type_label": {
        "English": "Type",
        "Hindi": "प्रकार",
        "Kannada": "ಪ್ರಕಾರ"
    },
    "file_size_label": {
        "English": "Size",
        "Hindi": "आकार",
        "Kannada": "ಗಾತ್ರ"
    },
    "target_lang_label": {
        "English": "Target Language",
        "Hindi": "लक्षित भाषा",
        "Kannada": "ಗುರಿ ಭಾಷೆ"
    },
    "status_extracting": {
        "English": "📤 Uploading and extracting document text...",
        "Hindi": "📤 दस्तावेज़ का पाठ निकाला जा रहा है...",
        "Kannada": "📤 ದಾಖಲೆಯ ಪಠ್ಯವನ್ನು ಹೊರತೆಗೆಯಲಾಗುತ್ತಿದೆ..."
    },
    "status_analyzing": {
        "English": "🤖 Analyzing document content with AI in {language}...",
        "Hindi": "🤖 {language} में एआई के साथ दस्तावेज़ सामग्री का विश्लेषण किया जा रहा है...",
        "Kannada": "🤖 {language} ನಲ್ಲಿ ಎಐ ಜೊತೆಗೆ ದಾಖಲೆಯ ವಿಷಯವನ್ನು ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ..."
    },
    "summary_heading": {
        "English": "📋 Document Summary",
        "Hindi": "📋 दस्तावेज़ सारांश",
        "Kannada": "📋 ದಾಖಲೆಯ ಸಾರಾಂಶ"
    },
    "critical_risks_label": {
        "English": "⚠️ Critical Note / Risks:",
        "Hindi": "⚠️ महत्वपूर्ण सूचना / जोखिम:",
        "Kannada": "⚠️ ಪ್ರಮುಖ ಸೂಚನೆ / ಅಪಾಯಗಳು:"
    },
    "ask_doc_header": {
        "English": "💬 Ask a question about this document",
        "Hindi": "💬 इस दस्तावेज़ के बारे में प्रश्न पूछें",
        "Kannada": "💬 ಈ ದಾಖಲೆಯ ಬಗ್ಗೆ ಪ್ರಶ್ನೆ ಕೇಳಿ"
    },
    "ask_doc_caption": {
        "English": "Answers are strictly grounded in your uploaded document ({filename}) in **{language}**.",
        "Hindi": "उत्तर पूरी तरह से आपके अपलोड किए गए दस्तावेज़ ({filename}) पर आधारित हैं **{language}** में।",
        "Kannada": "ಉತ್ತರಗಳು ನೀವು ಅಪ್‌ಲೋಡ್ ಮಾಡಿದ ದಾಖಲೆಯ ({filename}) ಆಧಾರದ ಮೇಲೆ ಮಾತ್ರ ನೀಡಲಾಗಿದೆ **{language}** ನಲ್ಲಿ."
    },
    "ask_doc_placeholder": {
        "English": "Ask any question about this document in {language}...",
        "Hindi": "{language} में इस दस्तावेज़ के बारे में कोई भी प्रश्न पूछें...",
        "Kannada": "{language} ನಲ್ಲಿ ಈ ದಾಖಲೆಯ ಬಗ್ಗೆ ಯಾವುದೇ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ..."
    },

    # ------------------ Government & Banking Guides Screens ------------------
    "proc_page_title": {
        "English": "🏛️ Government Process Guides",
        "Hindi": "🏛️ सरकारी प्रक्रिया मार्गदर्शिका",
        "Kannada": "🏛️ ಸರ್ಕಾರಿ ಪ್ರಕ್ರಿಯಾ ಮಾರ್ಗದರ್ಶಿಗಳು"
    },
    "proc_page_desc": {
        "English": "Select a common Indian citizen service below to view the complete step-by-step procedure, required documents, authority details, and fees.",
        "Hindi": "पूरी चरण-दर-चरण प्रक्रिया, आवश्यक दस्तावेज, प्राधिकरण विवरण और शुल्क देखने के लिए नीचे एक नागरिक सेवा का चयन करें।",
        "Kannada": "ಸಂಪೂರ್ಣ ಹಂತ-ಹಂತದ ಪ್ರಕ್ರಿಯೆ, ಅಗತ್ಯ ದಾಖಲೆಗಳು, ಪ್ರಾಧಿಕಾರದ ವಿವರಗಳು ಮತ್ತು ಶುಲ್ಕಗಳನ್ನು ವೀಕ್ಷಿಸಲು ಕೆಳಗೆ ಸಾಮಾನ್ಯ ಭಾರತೀಯ ನಾಗರಿಕ ಸೇವೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ."
    },
    "proc_selector_label": {
        "English": "📌 Select a Government Process Guide:",
        "Hindi": "📌 एक सरकारी प्रक्रिया गाइड चुनें:",
        "Kannada": "📌 ಸರ್ಕಾರಿ ಪ್ರಕ್ರಿಯಾ ಮಾರ್ಗದರ್ಶಿಯನ್ನು ಆಯ್ಕೆಮಾಡಿ:"
    },
    "banking_page_title": {
        "English": "🏦 Banking Service Guides",
        "Hindi": "🏦 बैंकिंग सेवा मार्गदर्शिका",
        "Kannada": "🏦 ಬ್ಯಾಂಕಿಂಗ್ ಸೇವಾ ಮಾರ್ಗದರ್ಶಿಗಳು"
    },
    "banking_page_desc": {
        "English": "Select a banking process below to view the complete step-by-step procedure, required documents, verification steps, and turnaround times.",
        "Hindi": "पूरी चरण-दर-चरण प्रक्रिया, आवश्यक दस्तावेज, सत्यापन चरण और समय-सीमा देखने के लिए नीचे एक बैंकिंग प्रक्रिया चुनें।",
        "Kannada": "ಸಂಪೂರ್ಣ ಹಂತ-ಹಂತದ ಪ್ರಕ್ರಿಯೆ, ಅಗತ್ಯ ದಾಖಲೆಗಳು, ಪರಿಶೀಲನಾ ಹಂತಗಳು ಮತ್ತು ಸಮಯಾವಧಿಯನ್ನು ವೀಕ್ಷಿಸಲು ಕೆಳಗೆ ಬ್ಯಾಂಕಿಂಗ್ ಪ್ರಕ್ರಿಯೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ."
    },
    "banking_selector_label": {
        "English": "📌 Select a Banking Guide:",
        "Hindi": "📌 एक बैंकिंग गाइड चुनें:",
        "Kannada": "📌 ಬ್ಯಾಂಕಿಂಗ್ ಮಾರ್ಗದರ್ಶಿಯನ್ನು ಆಯ್ಕೆಮಾಡಿ:"
    },
    "overview_label": {
        "English": "Overview",
        "Hindi": "अवलोकन",
        "Kannada": "ಅವಲೋಕನ"
    },
    "authority_office_header": {
        "English": "🏢 Authority & Office",
        "Hindi": "🏢 प्राधिकरण एवं कार्यालय",
        "Kannada": "🏢 ಪ್ರಾಧಿಕಾರ ಮತ್ತು ಕಚೇರಿ"
    },
    "mode_label": {
        "English": "Mode",
        "Hindi": "माध्यम",
        "Kannada": "ಮಾದರಿ"
    },
    "mode_both": {
        "English": "Online & Offline",
        "Hindi": "ऑनलाइन और ऑफलाइन",
        "Kannada": "ಆನ್‌ಲೈನ್ ಮತ್ತು ಆಫ್‌ಲೈನ್"
    },
    "state_variance_note": {
        "English": "*Note: confirm exact details at your nearest center, as requirements vary by state*",
        "Hindi": "*नोट: अपने नजदीकी केंद्र पर सटीक विवरण की पुष्टि करें, क्योंकि आवश्यकताएं राज्य के अनुसार भिन्न होती हैं*",
        "Kannada": "*ಗಮನಿಸಿ: ನಿಮ್ಮ ಹತ್ತಿರದ ಕೇಂದ್ರದಲ್ಲಿ ನಿಖರವಾದ ವಿವರಗಳನ್ನು ದೃಢೀಕರಿಸಿ, ಏಕೆಂದರೆ ಅಗತ್ಯತೆಗಳು ರಾಜ್ಯದಿಂದ ರಾಜ್ಯಕ್ಕೆ ಬದಲಾಗುತ್ತವೆ*"
    },
    "timeline_header": {
        "English": "⏱️ Estimated Timeline",
        "Hindi": "⏱️ अनुमानित समय-सीमा",
        "Kannada": "⏱️ ಅಂದಾಜು ಸಮಯಾವಧಿ"
    },
    "timeline_subtext": {
        "English": "Standard departmental turnaround time.",
        "Hindi": "मानक विभागीय प्रक्रिया समय।",
        "Kannada": "ಸಾಮಾನ್ಯ ಇಲಾಖೆಯ ಕಾರ್ಯನಿರ್ವಹಣಾ ಸಮಯ."
    },
    "fees_header": {
        "English": "💳 Prescribed Fees",
        "Hindi": "💳 निर्धारित शुल्क",
        "Kannada": "💳 ನಿಗದಿತ ಶುಲ್ಕಗಳು"
    },
    "fees_subtext": {
        "English": "Statutory application fees / charges.",
        "Hindi": "वैधानिक आवेदन शुल्क / प्रभार।",
        "Kannada": "ಶಾಸನಬದ್ಧ ಅರ್ಜಿ ಶುಲ್ಕಗಳು / ಶುಲ್ಕಗಳು."
    },
    "steps_procedure_header": {
        "English": "🪜 Step-by-Step Procedure",
        "Hindi": "🪜 चरण-दर-चरण प्रक्रिया",
        "Kannada": "🪜 ಹಂತ-ಹಂತದ ಕಾರ್ಯವಿಧಾನ"
    },
    "step_num_prefix": {
        "English": "Step",
        "Hindi": "चरण",
        "Kannada": "ಹಂತ"
    },
    "req_docs_header": {
        "English": "📑 Required Documents & Proofs",
        "Hindi": "📑 आवश्यक दस्तावेज एवं प्रमाण",
        "Kannada": "📑 ಅಗತ್ಯವಿರುವ ದಾಖಲೆಗಳು ಮತ್ತು ಪುರಾವೆಗಳು"
    },
    "ask_proc_header": {
        "English": "💬 Ask a question about this guide",
        "Hindi": "💬 इस गाइड के बारे में प्रश्न पूछें",
        "Kannada": "💬 ಈ ಮಾರ್ಗದರ್ಶಿಯ ಬಗ್ಗೆ ಪ್ರಶ್ನೆ ಕೇಳಿ"
    },
    "ask_proc_caption": {
        "English": "Answers are strictly grounded in this official process in **{language}**.",
        "Hindi": "उत्तर आधिकारिक प्रक्रिया पर आधारित हैं **{language}** में।",
        "Kannada": "ಉತ್ತರಗಳು ಅಧಿಕೃತ ಪ್ರಕ್ರಿಯೆಯ ಆಧಾರದ ಮೇಲೆ ಮಾತ್ರ ನೀಡಲಾಗಿದೆ **{language}** ನಲ್ಲಿ."
    },
    "ask_proc_placeholder": {
        "English": "Ask a question about {proc_name} in {language}...",
        "Hindi": "{language} में {proc_name} के बारे में एक प्रश्न पूछें...",
        "Kannada": "{language} ನಲ್ಲಿ {proc_name} ಕುರಿತು ಪ್ರಶ್ನೆ ಕೇಳಿ..."
    },

    # ------------------ Dashboard Screen ------------------
    "tab_summary": {
        "English": "Summary",
        "Hindi": "सारांश",
        "Kannada": "ಸಾರಾಂಶ"
    },
    "tab_steps": {
        "English": "Steps",
        "Hindi": "चरण",
        "Kannada": "ಹಂತಗಳು"
    },
    "tab_deadlines_docs": {
        "English": "Deadlines & Documents",
        "Hindi": "समय-सीमा और दस्तावेज",
        "Kannada": "ಗಡುವುಗಳು ಮತ್ತು ದಾಖಲೆಗಳು"
    },
    "tab_qa": {
        "English": "Ask a Question",
        "Hindi": "प्रश्न पूछें",
        "Kannada": "ಪ್ರಶ್ನೆ ಕೇಳಿ"
    },
    "exec_summary_header": {
        "English": "📌 Executive Summary",
        "Hindi": "📌 कार्यकारी सारांश",
        "Kannada": "📌 ಕಾರ್ಯಕಾರಿ ಸಾರಾಂಶ"
    },
    "action_checklist_header": {
        "English": "🪜 Action Checklist & Next Steps",
        "Hindi": "🪜 कार्य चेकलिस्ट और अगले कदम",
        "Kannada": "🪜 ಕ್ರಿಯಾ ಪರಿಶೀಲನಾಪಟ್ಟಿ ಮತ್ತು ಮುಂದಿನ ಹಂತಗಳು"
    },
    "action_checklist_subtext": {
        "English": "Mark items off as you complete them. Your progress is saved automatically across tab switches.",
        "Hindi": "जैसे ही आप उन्हें पूरा करते हैं, आइटमों को चिह्नित करें। आपकी प्रगति टैब स्विच में सहेजी जाती है।",
        "Kannada": "ನೀವು ಪೂರ್ಣಗೊಳಿಸಿದಂತೆ ಐಟಂಗಳನ್ನು ಗುರುತಿಸಿ. ನಿಮ್ಮ ಪ್ರಗತಿಯು ಸ್ವಯಂಚಾಲಿತವಾಗಿ ಉಳಿಸಲ್ಪಡುತ್ತದೆ."
    },
    "deadlines_header": {
        "English": "⏰ Important Deadlines & Timelines",
        "Hindi": "⏰ महत्वपूर्ण समय-सीमा और तिथियां",
        "Kannada": "⏰ ಪ್ರಮುಖ ಗಡುವುಗಳು ಮತ್ತು ಸಮಯಾವಧಿಗಳು"
    },
    "no_deadlines_info": {
        "English": "No strict deadlines mentioned in the document.",
        "Hindi": "दस्तावेज़ में कोई सख्त समय-सीमा उल्लिखित नहीं है।",
        "Kannada": "ದಾಖಲೆಯಲ್ಲಿ ಯಾವುದೇ ಕಟ್ಟುನಿಟ್ಟಾದ ಗಡುವುಗಳನ್ನು ಉಲ್ಲೇಖಿಸಲಾಗಿಲ್ಲ."
    },
    "no_docs_info": {
        "English": "No specific supporting documents required.",
        "Hindi": "किसी विशिष्ट सहायक दस्तावेज़ की आवश्यकता नहीं है।",
        "Kannada": "ಯಾವುದೇ ನಿರ್ದಿಷ್ಟ ಪೋಷಕ ದಾಖಲೆಗಳು ಅಗತ್ಯವಿಲ್ಲ."
    },
    "no_steps_info": {
        "English": "No specific action steps required.",
        "Hindi": "किसी विशिष्ट कार्रवाई चरण की आवश्यकता नहीं है।",
        "Kannada": "ಯಾವುದೇ ನಿರ್ದಿಷ್ಟ ಕ್ರಿಯೆಯ ಹಂತಗಳು ಅಗತ್ಯವಿಲ್ಲ."
    },
    "doc_origin_header": {
        "English": "🏛️ Document Origin",
        "Hindi": "🏛️ दस्तावेज़ मूल",
        "Kannada": "🏛️ ದಾಖಲೆಯ ಮೂಲ"
    },
    "doc_origin_desc": {
        "English": "Issued by competent jurisdiction or official organization referenced in document.",
        "Hindi": "दस्तावेज़ में संदर्भित सक्षम क्षेत्राधिकार या आधिकारिक संगठन द्वारा जारी किया गया।",
        "Kannada": "ದಾಖಲೆಯಲ್ಲಿ ಉಲ್ಲೇಖಿಸಲಾದ ಸಮರ್ಥ ನ್ಯಾಯವ್ಯಾಪ್ತಿ ಅಥವಾ ಅಧಿಕೃತ ಸಂಸ್ಥೆಯಿಂದ ನೀಡಲಾಗಿದೆ."
    },
    "no_doc_loaded_warning": {
        "English": "⚠️ No document or government process is currently loaded.",
        "Hindi": "⚠️ वर्तमान में कोई दस्तावेज़ या सरकारी प्रक्रिया लोड नहीं है।",
        "Kannada": "⚠️ ಪ್ರಸ್ತುತ ಯಾವುದೇ ದಾಖಲೆ ಅಥವಾ ಸರ್ಕಾರಿ ಪ್ರಕ್ರಿಯೆಯನ್ನು ಲೋಡ್ ಮಾಡಲಾಗಿಲ್ಲ."
    },
    "no_doc_loaded_info": {
        "English": "Please upload a document on the **Home** page or choose a guide from the **Government Services** section.",
        "Hindi": "कृपया **होम** पेज पर दस्तावेज़ अपलोड करें या **सरकारी सेवाएं** अनुभाग से गाइड चुनें।",
        "Kannada": "ದಯವಿಟ್ಟು **ಮುಖಪುಟ** ಪುಟದಲ್ಲಿ ದಾಖಲೆಯನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ಅಥವಾ **ಸರ್ಕಾರಿ ಸೇವೆಗಳು** ವಿಭಾಗದಿಂದ ಮಾರ್ಗದರ್ಶಿಯನ್ನು ಆಯ್ಕೆಮಾಡಿ."
    },

    # ------------------ Placeholder Pages ------------------
    "current_task_title": {
        "English": "📋 Current Task",
        "Hindi": "📋 वर्तमान कार्य",
        "Kannada": "📋 ಪ್ರಸ್ತುತ ಕಾರ್ಯ"
    },
    "no_active_task_info": {
        "English": "ℹ️ No active document or government process task in progress.",
        "Hindi": "ℹ️ कोई सक्रिय दस्तावेज़ या सरकारी प्रक्रिया कार्य प्रगति पर नहीं है।",
        "Kannada": "ℹ️ ಯಾವುದೇ ಸಕ್ರಿಯ ದಾಖಲೆ ಅಥವಾ ಸರ್ಕಾರಿ ಪ್ರಕ್ರಿಯಾ ಕಾರ್ಯ ಪ್ರಗತಿಯಲ್ಲಿಲ್ಲ."
    },
    "no_active_task_desc": {
        "English": "Please choose an option from the **Home** screen to start a new task.",
        "Hindi": "नया कार्य शुरू करने के लिए कृपया **होम** स्क्रीन से एक विकल्प चुनें।",
        "Kannada": "ಹೊಸ ಕಾರ್ಯವನ್ನು ಪ್ರಾರಂಭಿಸಲು ದಯವಿಟ್ಟು **ಮುಖಪುಟ** ಪರದೆಯಿಂದ ಆಯ್ಕೆಯನ್ನು ಆರಿಸಿ."
    },
    "completed_task_title": {
        "English": "✅ Completed Tasks",
        "Hindi": "✅ पूर्ण कार्य",
        "Kannada": "✅ ಪೂರ್ಣಗೊಂಡ ಕಾರ್ಯಗಳು"
    },
    "completed_tasks_count": {
        "English": "🎉 You have completed {count} action item(s) in your current session.",
        "Hindi": "🎉 आपने अपने वर्तमान सत्र में {count} कार्य आइटम पूरे कर लिए हैं।",
        "Kannada": "🎉 ನಿಮ್ಮ ಪ್ರಸ್ತುತ ಅವಧಿಯಲ್ಲಿ ನೀವು {count} ಕ್ರಿಯಾ ಐಟಂಗಳನ್ನು ಪೂರ್ಣಗೊಳಿಸಿದ್ದೀರಿ."
    },
    "no_completed_tasks_info": {
        "English": "ℹ️ No completed tasks yet. Completed action steps will appear here as you check them off.",
        "Hindi": "ℹ️ अभी तक कोई पूर्ण कार्य नहीं है। पूर्ण किए गए चरण यहां दिखाई देंगे।",
        "Kannada": "ℹ️ ಇನ್ನೂ ಯಾವುದೇ ಪೂರ್ಣಗೊಂಡ ಕಾರ್ಯಗಳಿಲ್ಲ. ನೀವು ಅವುಗಳನ್ನು ಗುರುತಿಸಿದಂತೆ ಪೂರ್ಣಗೊಂಡ ಹಂತಗಳು ಇಲ್ಲಿ ಗೋಚರಿಸುತ್ತವೆ."
    }
}

def get_normalized_language(language_input: str = None) -> str:
    """
    Standardizes language strings to 'English', 'Hindi', or 'Kannada'.
    """
    if language_input is None:
        try:
            language_input = st.session_state.get("language", "English")
        except Exception:
            language_input = "English"
            
    lang_str = str(language_input)
    if "Hindi" in lang_str or "हिंदी" in lang_str:
        return "Hindi"
    elif "Kannada" in lang_str or "ಕನ್ನಡ" in lang_str:
        return "Kannada"
    return "English"

class SafeFormatter(string.Formatter):
    def __init__(self, default_lang="English"):
        self.default_lang = default_lang
        
    def get_value(self, key, args, kwargs):
        if isinstance(key, str):
            if key in kwargs:
                return kwargs[key]
            if key == "language":
                return self.default_lang
            if key == "proc_name":
                return "Guide"
            if key == "filename":
                return "Document"
            if key == "user_name":
                return "User"
            if key == "count":
                return "0"
            return ""
        return super().get_value(key, args, kwargs)

def t(key: str, language: str = None, **kwargs) -> str:
    """
    Looks up translation key in TRANSLATIONS dictionary.
    Falls back to English if missing, printing a warning to the console.
    Applies string formatting with kwargs safely.
    """
    active_lang = get_normalized_language(language)
    entry = TRANSLATIONS.get(key)
    
    if entry is None:
        print(f"[Translation Warning] Missing key '{key}'")
        text = key
    else:
        text = entry.get(active_lang)
        if text is None:
            text = entry.get("English", key)

    formatter = SafeFormatter(default_lang=active_lang)
    try:
        text = formatter.vformat(text, (), kwargs)
    except Exception as e:
        print(f"[Translation Format Warning] Key '{key}': {e}")
            
    return text


# Dynamically add insurance keys
TRANSLATIONS.update({"insurance_page_title": {"English": "🛡️ Insurance Service Guides", "Hindi": "🛡️ बीमा सेवा मार्गदर्शिका", "Kannada": "🛡️ ವಿಮಾ ಸೇವಾ ಮಾರ್ಗದರ್ಶಿಗಳು"}, "insurance_page_desc": {"English": "Select an insurance topic below to view the complete claim process, policy breakdown, coverage checklists, and required documents.", "Hindi": "पूरी दावा प्रक्रिया, पॉलिसी विवरण, कवरेज चेकलिस्ट और आवश्यक दस्तावेज देखने के लिए नीचे एक बीमा विषय चुनें।", "Kannada": "ಸಂಪೂರ್ಣ ಕ್ಲೈಮ್ ಪ್ರಕ್ರಿಯೆ, ಪಾಲಿಸಿ ವಿವರಣೆ, ಕವರೇಜ್ ಪರಿಶೀಲನಾಪಟ್ಟಿಗಳು ಮತ್ತು ಅಗತ್ಯ ದಾಖಲೆಗಳನ್ನು ವೀಕ್ಷಿಸಲು ಕೆಳಗೆ ವಿಮಾ ವಿಷಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ."}, "insurance_selector_label": {"English": "📌 Select an Insurance Guide:", "Hindi": "📌 एक बीमा गाइड चुनें:", "Kannada": "📌 ವಿಮಾ ಮಾರ್ಗದರ್ಶಿಯನ್ನು ಆಯ್ಕೆಮಾಡಿ:"}})

TRANSLATIONS.update({"start_over": {"English": "🔄 Start Over", "Hindi": "🔄 पुनः प्रारंभ करें", "Kannada": "🔄 ಮೊದಲಿನಿಂದ ಪ್ರಾರಂಭಿಸಿ"}, "open_dashboard_btn": {"English": "🚀 Open in Action Dashboard ➔", "Hindi": "🚀 एक्शन डैशबोर्ड में खोलें ➔", "Kannada": "🚀 ಕ್ರಿಯಾ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ನಲ್ಲಿ ತೆರೆಯಿರಿ ➔"}})

TRANSLATIONS.update({"select_loan_type": {"English": "📋 Select Loan Category:", "Hindi": "📋 ऋण श्रेणी चुनें:", "Kannada": "📋 ಸಾಲದ ವರ್ಗವನ್ನು ಆಯ್ಕೆಮಾಡಿ:"}, "select_bank": {"English": "🏦 Select Bank / Lending Institution:", "Hindi": "🏦 बैंक / ऋणदाता संस्थान चुनें:", "Kannada": "🏦 ಬ್ಯಾಂಕ್ / ಸಾಲ ನೀಡುವ ಸಂಸ್ಥೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ:"}, "loan_guidance_header": {"English": "🏦 Bank-Specific Loan Guidance", "Hindi": "🏦 बैंक-विशिष्ट ऋण मार्गदर्शन", "Kannada": "🏦 ಬ್ಯಾಂಕ್-ನಿರ್ದಿಷ್ಟ ಸಾಲ ಮಾರ್ಗದರ್ಶನ"}, "loan_disclaimer_label": {"English": "⚠️ Important Bank Advisory & Rate Notice:", "Hindi": "⚠️ महत्वपूर्ण बैंक सलाह और ब्याज दर सूचना:", "Kannada": "⚠️ ಪ್ರಮುಖ ಬ್ಯಾಂಕ್ ಸಲಹೆ ಮತ್ತು ದರ ಸೂಚನೆ:"}})

TRANSLATIONS.update({"cat_documents": {"English": "📁 Uploaded Documents", "Hindi": "📁 अपलोड किए गए दस्तावेज़", "Kannada": "📁 ಅಪ್‌ಲೋಡ್ ಮಾಡಲಾದ ದಾಖಲೆಗಳು"}, "cat_government": {"English": "🏛️ Government Services", "Hindi": "🏛️ सरकारी सेवाएं", "Kannada": "🏛️ ಸರ್ಕಾರಿ ಸೇವೆಗಳು"}, "cat_banking": {"English": "🏦 Banking Services", "Hindi": "🏦 बैंकिंग सेवाएं", "Kannada": "🏦 ಬ್ಯಾಂಕಿಂಗ್ ಸೇವೆಗಳು"}, "cat_insurance": {"English": "🛡️ Insurance Services", "Hindi": "🛡️ बीमा सेवाएं", "Kannada": "🛡️ ವಿಮಾ ಸೇವೆಗಳು"}, "no_completed_in_category": {"English": "No completed tasks in this category yet.", "Hindi": "इस श्रेणी में अभी तक कोई पूर्ण कार्य नहीं है।", "Kannada": "ಈ ವರ್ಗದಲ್ಲಿ ಇನ್ನೂ ಯಾವುದೇ ಪೂರ್ಣಗೊಂಡ ಕಾರ್ಯಗಳಿಲ್ಲ."}, "no_completed_tasks_desc": {"English": "As you complete steps or analyze documents across Government, Banking, Insurance, and Document Uploads, they will be organized here by category.", "Hindi": "जैसे ही आप सरकारी, बैंकिंग, बीमा और दस्तावेज़ अपलोड में चरणों को पूरा करते हैं, वे यहाँ श्रेणी के अनुसार व्यवस्थित होंगे।", "Kannada": "ನೀವು ಸರ್ಕಾರಿ, ಬ್ಯಾಂಕಿಂಗ್, ವಿಮೆ ಮತ್ತು ದಾಖಲೆ ಅಪ್‌ಲೋಡ್‌ಗಳಲ್ಲಿ ಹಂತಗಳನ್ನು ಪೂರ್ಣಗೊಳಿಸಿದಂತೆ, ಅವುಗಳನ್ನು ಇಲ್ಲಿ ವರ್ಗವಾರು ಆಯೋಜಿಸಲಾಗುತ್ತದೆ."}})
