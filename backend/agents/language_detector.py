"""
Language detection agent using Agno.
Explicitly configured with Qubrid GPT-OSS-20B model.
"""
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from backend.llm import detect_language
import os


def create_language_detection_agent() -> Agent:
    """
    Create an Agno agent for language detection.
    
    Uses Qubrid's GPT-OSS-20B model with explicit configuration.
    No implicit OpenAI dependencies.
    
    Returns:
        Configured Agno Agent
    """
    # Explicit Qubrid model configuration
    qubrid_model = OpenAIChat(
        id="openai/gpt-oss-20b",
        api_key=os.getenv("QUBRID_API_KEY"),
        base_url=os.getenv("QUBRID_CHAT_URL"),
    )
    
    return Agent(
        name="Language Detection Specialist",
        model=qubrid_model,
        instructions=[
            "You are a language detection specialist.",
            "When given text, you must detect its language.",
            "Call the detect_language function with the provided text.",
            "Return only the detected language name.",
        ],
        markdown=True,
    )


def detect_language_function(text: str) -> str:
    """
    Function that Agno agent will call for language detection.
    Wraps the infrastructure layer's detect_language.
    """
    result = detect_language(text)
    return f"Language: {result['source_language']}, Multilingual: {result['is_multilingual']}"

