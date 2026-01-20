"""
Translation agent using Agno.
Explicitly configured with Qubrid GPT-OSS-20B model.
"""
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from backend.llm import translate_text
import os


def create_translation_agent() -> Agent:
    """
    Create an Agno agent for translation.
    
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
        name="Translation Specialist",
        model=qubrid_model,
        instructions=[
            "You are a translation specialist.",
            "When given text and a target language, you must translate the text.",
            "Call the translate_text function with the text and target language.",
            "Return only the translated text.",
        ],
        markdown=True,
    )


def translate_text_function(text: str, target_language: str) -> str:
    """
    Function that Agno agent will call for translation.
    Wraps the infrastructure layer's translate_text.
    """
    result = translate_text(text, target_language)
    return result["translated_text"]

