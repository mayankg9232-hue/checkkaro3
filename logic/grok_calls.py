from logic.llm_calls import general_chat_answer

def general_answer(question: str, language: str = "English") -> str:
    """
    Answers general user questions using the active LLM engine (Groq / Anthropic).
    """
    return general_chat_answer(question, language=language)
