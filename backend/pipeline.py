"""
Translation pipeline orchestration.
Simple Python controller - no framework magic.
"""
from typing import Dict, Any
from backend.llm import detect_language, translate_text


class TranslationPipeline:
    """
    Orchestrates the translation workflow using direct function calls.
    
    Pipeline:
    1. Detect language using Qubrid GPT-OSS-20B
    2. Translate text using Qubrid GPT-OSS-20B
    
    No agent framework overhead - just explicit Python execution.
    """
    
    def __init__(self):
        """Initialize the translation pipeline."""
        pass
    
    def translate(self, text: str, target_language: str) -> Dict[str, Any]:
        """
        Execute the translation pipeline.
        
        Args:
            text: Text to translate
            target_language: Target language name or code
            
        Returns:
            Dict containing:
                - success: Whether translation succeeded
                - detected_language: Source language
                - translated_text: Translation result
                - error: Error message if failed
        """
        try:
            # Step 1: Language Detection
            detection_result = detect_language(text)
            detected_lang = detection_result.get("source_language", "Unknown")
            is_multilingual = detection_result.get("is_multilingual", False)
            
            # Step 2: Translation
            translation_result = translate_text(text, target_language)
            translated = translation_result.get("translated_text", "")
            
            return {
                "success": True,
                "detected_language": detected_lang,
                "is_multilingual": is_multilingual,
                "translated_text": translated,
                "raw_output": translated
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "detected_language": None,
                "translated_text": None
            }

