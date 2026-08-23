import streamlit as st
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
