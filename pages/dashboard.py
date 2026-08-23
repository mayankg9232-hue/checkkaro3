import streamlit as st
from logic.llm_calls import answer_question
from logic.memory_manager import log_qa, get_qa_history_for_document, format_for_streamlit_chat
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
        
        doc_id = st.session_state.get("uploaded_file_name", doc_type_title)
        context_text = st.session_state.get("doc_text", "")
        if not context_text:
            context_text = str(result)
            
        # Synchronize chat history from memory manager
        if "chat_history" not in st.session_state or st.session_state.get("chat_doc_id") != doc_id:
            doc_history = get_qa_history_for_document(doc_id)
            st.session_state["chat_history"] = format_for_streamlit_chat(doc_history)
            st.session_state["chat_doc_id"] = doc_id

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
                    answer = answer_question(
                        context_text,
                        user_query,
                        language=current_lang,
                        history=st.session_state.get('chat_history', [])[:-1]
                    )
                    st.write(answer)
                    st.session_state["chat_history"].append({"role": "assistant", "content": answer})
                    # Persist to QA memory database
                    log_qa(
                        context_type="document",
                        context_id=doc_id,
                        question=user_query,
                        answer=answer,
                        language=current_lang
                    )
