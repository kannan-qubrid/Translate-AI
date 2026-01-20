import streamlit as st
from typing import Dict, Any
from backend.db import init_db, get_all_chat_ids, delete_chat

def render_welcome_screen():
    """Render welcome screen when no conversation is active."""
    st.title("🌐 Image Translation AI")
    st.write("Extract and translate text from any image using OCR and GPT-OSS-20B.")
    
    with st.expander("How it works", expanded=True):
        st.write("1. **Upload an image** (PNG, JPG, or JPEG)")
        st.write("2. **Select Target Language** in the sidebar")
        st.write("3. **AI extracts text** using Hunyuan OCR")
        st.write("4. **AI translates text** using GPT-OSS-20B")
        st.write("5. **History persists** automatically to SQLite")


def render_sidebar() -> Dict[str, Any]:
    """Render sidebar with conversation history and model controls."""
    
    # Initialize DB (can be called multiple times safely)
    init_db()
    
    st.sidebar.subheader("💬 Chat History")
    
    # Load past chats from SQLite
    past_chats = get_all_chat_ids()
    active_id = st.session_state.get("active_chat_id")
    
    if past_chats:
        for chat in past_chats:
            is_active = chat["chat_id"] == active_id
            col1, col2 = st.sidebar.columns([4, 1])
            with col1:
                if st.button(
                    f"📝 {chat['title'][:15]}...",
                    key=f"chat_{chat['chat_id']}",
                    width="stretch",
                    type="primary" if is_active else "secondary"
                ):
                    st.session_state.active_chat_id = chat["chat_id"]
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"del_{chat['chat_id']}", width="stretch"):
                    delete_chat(chat["chat_id"])
                    if is_active:
                        st.session_state.active_chat_id = None
                        st.session_state.messages = []
                    st.rerun()
    else:
        st.sidebar.info("No saved chats")

    st.sidebar.divider()
    
    # Target Language Selector
    languages = {
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "it": "Italian",
        "pt": "Portuguese",
        "hi": "Hindi",
        "zh": "Chinese",
        "ja": "Japanese",
        "ko": "Korean",
        "ru": "Russian",
        "ar": "Arabic"
    }
    
    target_lang = st.sidebar.selectbox(
        "🎯 Target Language",
        options=list(languages.keys()),
        format_func=lambda x: f"{languages[x]} ({x})",
        index=0
    )
    
    with st.sidebar.expander("⚙️ Model Settings", expanded=False):
        temperature = st.slider("Temperature", 0.0, 2.0, st.session_state.get("_temperature", 0.7), 0.1)
        st.session_state._temperature = temperature

    uploaded_file = st.sidebar.file_uploader("📤 Upload Image", type=["png", "jpg", "jpeg"])
    
    st.sidebar.divider()
    
    if st.sidebar.button("🔄 New Chat", width="stretch", type="primary"):
        st.session_state.active_chat_id = None
        st.rerun()
    
    return {
        "temperature": temperature,
        "target_language": target_lang,
        "uploaded_file": uploaded_file
    }

    uploaded_file = st.sidebar.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    st.sidebar.divider()
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("New Chat", width="stretch", type="primary"):
            st.session_state.active_conversation_id = None
            st.session_state.chat_memory.clear()
            st.rerun()
    with col2:
        if st.button("Reset Params", width="stretch"):
            for key in ["_temperature", "_max_tokens", "_top_p", "_top_k", "_presence_penalty"]:
                st.session_state.pop(key, None)
            st.rerun()
    
    return {
        "stream": True,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p,
        "top_k": top_k,
        "presence_penalty": presence_penalty,
        "uploaded_file": uploaded_file
    }
