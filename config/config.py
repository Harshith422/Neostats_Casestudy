import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL   = "llama-3.1-8b-instant"

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

CHUNK_SIZE         = 500
CHUNK_OVERLAP      = 50
TOP_K_RESULTS      = 4
SIMILARITY_THRESHOLD = 0.3

APP_TITLE     = "LearnMate AI"
APP_ICON      = ""
APP_SUBTITLE  = "Intelligent Study Partner"
MAX_MESSAGES  = 50
