import streamlit as st
import time
from logic.extract_text import extract_text_with_metadata
from logic.llm_calls import analyze_document, answer_question
from logic.memory_manager import log_qa, get_qa_history_for_document, format_for_streamlit_chat
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
                extracted_text, metadata = extract_text_with_metadata(uploaded_file, uploaded_file.name)
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
            st.session_state["doc_metadata"] = metadata
            st.session_state["analysis_result"] = analysis
            st.session_state["context_raw"] = extracted_text
            st.session_state["uploaded_file_name"] = uploaded_file.name
            st.session_state["analyzed_language"] = current_lang
            
            # Load stored document Q&A history from memory manager
            doc_history = get_qa_history_for_document(uploaded_file.name)
            st.session_state["chat_history"] = format_for_streamlit_chat(doc_history)
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
    metadata = st.session_state.get("doc_metadata", {})

    with stage_placeholder.container():
        # Display calm note if low-text / image pages were skipped
        low_pages = metadata.get("low_text_pages", [])
        if low_pages:
            pages_str = ", ".join(map(str, low_pages))
            st.info(f"ℹ️ Note: Page(s) {pages_str} contained image-only content with no readable text and were skipped, while all readable text across the remaining pages was fully scanned.")

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

    # Synchronize chat history from memory manager if empty or switching
    if "chat_history" not in st.session_state or st.session_state.get("chat_doc_id") != uploaded_file.name:
        doc_history = get_qa_history_for_document(uploaded_file.name)
        st.session_state["chat_history"] = format_for_streamlit_chat(doc_history)
        st.session_state["chat_doc_id"] = uploaded_file.name

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
                answer = answer_question(
                    extracted_text,
                    user_q,
                    language=current_lang,
                    history=st.session_state.get("chat_history", [])[:-1]
                )
                st.write(answer)
                st.session_state["chat_history"].append({"role": "assistant", "content": answer})
                # Persist to QA memory database
                log_qa(
                    context_type="document",
                    context_id=uploaded_file.name,
                    question=user_q,
                    answer=answer,
                    language=current_lang
                )
