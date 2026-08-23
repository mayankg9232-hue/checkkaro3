from typing import Optional, List, Dict
from logic.llm_calls import general_chat_answer

def general_answer(
    question: str,
    language: str = "English",
    history: Optional[List[Dict[str, str]]] = None
) -> str:
    """
    Answers general citizen user questions using the active LLM engine (Groq / Anthropic)
    with conversation history support and localized prompt adherence.
    """
    return general_chat_answer(question, history=history, language=language)
