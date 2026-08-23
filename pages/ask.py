import streamlit as st
from logic.grok_calls import general_answer
from logic.memory_manager import log_qa, get_general_qa_history, format_for_streamlit_chat
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

    # Synchronize general chat history from memory manager
    if "general_chat_history" not in st.session_state or st.session_state.get("general_chat_loaded") is not True:
        gen_history = get_general_qa_history()
        st.session_state["general_chat_history"] = format_for_streamlit_chat(gen_history)
        st.session_state["general_chat_loaded"] = True

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
                answer = general_answer(
                    user_q,
                    language=current_lang,
                    history=st.session_state.get("general_chat_history", [])[:-1]
                )
                st.write(answer)
                st.session_state["general_chat_history"].append({"role": "assistant", "content": answer})
                # Persist to QA memory database
                log_qa(
                    context_type="general",
                    context_id="general",
                    question=user_q,
                    answer=answer,
                    language=current_lang
                )
