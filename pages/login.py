import streamlit as st
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
