import streamlit as st
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
