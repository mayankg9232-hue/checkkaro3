import os
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(DB_DIR, "qa_history.db")

def get_db_connection() -> sqlite3.Connection:
    """
    Returns a thread-safe connection to the SQLite QA history database.
    """
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Initializes the SQLite schema for storing multi-context QA history.
    """
    conn = get_db_connection()
    try:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS qa_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    context_type TEXT NOT NULL,
                    context_id TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    language TEXT NOT NULL DEFAULT 'English',
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                );
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_qa_context 
                ON qa_history(context_type, context_id);
            """)
    finally:
        conn.close()

# Auto-initialize DB on import
init_db()

def log_qa(
    context_type: str,
    context_id: str,
    question: str,
    answer: str,
    language: str = "English",
    metadata: Optional[Dict[str, Any]] = None
) -> int:
    """
    Persists a question-and-answer exchange into the QA history database.
    
    Args:
        context_type: 'document', 'government', 'banking', 'insurance', 'general'
        context_id: Document filename/ID, Process ID, or 'general'
        question: User query string
        answer: Assistant response string
        language: Language code/name used for the exchange
        metadata: Optional dictionary with extra context (e.g. loan parameters)
        
    Returns:
        The row ID of the inserted record.
    """
    if not question or not answer:
        return -1

    conn = get_db_connection()
    meta_json = json.dumps(metadata) if metadata else None
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO qa_history (context_type, context_id, question, answer, language, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                str(context_type).strip().lower(),
                str(context_id).strip(),
                str(question).strip(),
                str(answer).strip(),
                str(language).strip(),
                meta_json
            ))
            return cursor.lastrowid
    finally:
        conn.close()

def get_qa_history(
    context_type: Optional[str] = None,
    context_id: Optional[str] = None,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Retrieves QA history entries matching the given context filters, ordered chronologically.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = "SELECT id, context_type, context_id, question, answer, language, timestamp, metadata FROM qa_history WHERE 1=1"
        params = []
        
        if context_type:
            query += " AND context_type = ?"
            params.append(str(context_type).strip().lower())
            
        if context_id:
            query += " AND context_id = ?"
            params.append(str(context_id).strip())
            
        query += " ORDER BY id ASC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        results = []
        for r in rows:
            meta = None
            if r["metadata"]:
                try:
                    meta = json.loads(r["metadata"])
                except Exception:
                    meta = r["metadata"]
            results.append({
                "id": r["id"],
                "context_type": r["context_type"],
                "context_id": r["context_id"],
                "question": r["question"],
                "answer": r["answer"],
                "language": r["language"],
                "timestamp": r["timestamp"],
                "metadata": meta
            })
        return results
    finally:
        conn.close()

def get_qa_history_for_document(document_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    """
    Retrieves QA history for a specific uploaded document.
    """
    return get_qa_history(context_type="document", context_id=document_id, limit=limit)

def get_qa_history_for_process(category: str, process_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    """
    Retrieves QA history for a specific curated process (government, banking, insurance).
    """
    return get_qa_history(context_type=category, context_id=process_id, limit=limit)

def get_general_qa_history(limit: int = 50) -> List[Dict[str, Any]]:
    """
    Retrieves general citizen assistant QA history.
    """
    return get_qa_history(context_type="general", context_id="general", limit=limit)

def format_for_streamlit_chat(records: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    Converts database QA records into Streamlit chat message format:
    [{"role": "user", "content": ...}, {"role": "assistant", "content": ...}]
    """
    chat_messages = []
    for r in records:
        if r.get("question"):
            chat_messages.append({"role": "user", "content": r["question"]})
        if r.get("answer"):
            chat_messages.append({"role": "assistant", "content": r["answer"]})
    return chat_messages

def clear_qa_history(context_type: Optional[str] = None, context_id: Optional[str] = None):
    """
    Clears QA history entries. Used for testing or user-initiated reset.
    """
    conn = get_db_connection()
    try:
        with conn:
            if context_type and context_id:
                conn.execute("DELETE FROM qa_history WHERE context_type = ? AND context_id = ?", (str(context_type).strip().lower(), str(context_id).strip()))
            elif context_type:
                conn.execute("DELETE FROM qa_history WHERE context_type = ?", (str(context_type).strip().lower(),))
            elif context_id:
                conn.execute("DELETE FROM qa_history WHERE context_id = ?", (str(context_id).strip(),))
            else:
                conn.execute("DELETE FROM qa_history")
    finally:
        conn.close()
