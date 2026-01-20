"""
Global UI configuration for Vision AI.
Reverted to Streamlit default theme.
"""

def get_base_css() -> str:
    """
    Returns empty string to revert to default Streamlit theme.
    """
    return ""


# Font size constants (preserving if needed for other components, but mostly ignored now)
FONT_SIZES = {
    "app_title": "42px",
    "section_header": "18px",
    "chat_text": "14px",
    "helper_text": "12px",
    "button_text": "14px",
}

# Color constants (preserving if needed for other components, but mostly ignored now)
COLORS = {
    "background": "#1a0b2e",
    "sidebar_bg": "#2a1a4a",
    "element_bg": "#3a2a5a",
    "border": "#4a3a6a",
    "text_primary": "#FFFFFF",
    "text_secondary": "#E0E0E0",
}
