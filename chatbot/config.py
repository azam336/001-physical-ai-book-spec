import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the chatbot directory
load_dotenv(Path(__file__).parent / ".env")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Qdrant
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
QDRANT_COLLECTION = "physical_ai_book"

# Models
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536
CHAT_MODEL = "gpt-4o-mini"

# CORS
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    if origin.strip()
]

# Docs path (relative to chatbot directory)
DOCS_DIR = Path(__file__).parent.parent / "docs"
