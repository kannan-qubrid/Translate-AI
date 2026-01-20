"""Database module for conversation persistence."""
from .sqlite import (
    init_db,
    save_message,
    get_chat_history,
    get_all_chat_ids,
    delete_chat
)

__all__ = [
    "init_db",
    "save_message",
    "get_chat_history",
    "get_all_chat_ids",
    "delete_chat"
]
