import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any

DB_PATH = "translation_chat.db"

def init_db():
    """Initialize the SQLite database and create tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_message(chat_id: str, role: str, content: str):
    """Save a message to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO conversations (chat_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
        (chat_id, role, content, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def get_chat_history(chat_id: str) -> List[Dict[str, Any]]:
    """Retrieve chat history for a specific chat_id."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content FROM conversations WHERE chat_id = ? ORDER BY timestamp ASC",
        (chat_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [{"role": row["role"], "content": row["content"]} for row in rows]

def get_all_chat_ids() -> List[Dict[str, Any]]:
    """Retrieve all unique chat_ids and their latest titles (first message)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # Get the first 'user' message as the title for each chat_id
    cursor.execute("""
        SELECT chat_id, content as title, MIN(timestamp)
        FROM conversations
        WHERE role = 'user'
        GROUP BY chat_id
        ORDER BY MIN(timestamp) DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [{"chat_id": row["chat_id"], "title": row["title"]} for row in rows]
def delete_chat(chat_id: str):
    """Delete all messages for a specific chat_id."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM conversations WHERE chat_id = ?", (chat_id,))
    conn.commit()
    conn.close()
