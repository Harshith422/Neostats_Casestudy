import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_groq import ChatGroq
from config.config import GROQ_API_KEY, GROQ_MODEL

def get_llm():
    """Initializes and returns the Groq LLaMA model."""
    try:
        model = ChatGroq(
            api_key=GROQ_API_KEY,
            model=GROQ_MODEL,
            temperature=0.7,
        )
        return model
    except Exception as e:
        raise RuntimeError(f"Could not load the AI model: {str(e)}")