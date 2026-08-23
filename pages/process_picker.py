import streamlit as st
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
