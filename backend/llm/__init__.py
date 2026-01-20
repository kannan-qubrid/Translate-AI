"""LLM module for language detection and translation."""
from .qubrid_client import detect_language, translate_text

__all__ = ["detect_language", "translate_text"]
