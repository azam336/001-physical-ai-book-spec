import os
from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

COLLECTION_NAME = "001-physical-ai-book-spec"
EMBEDDING_MODEL = "text-embedding-3-small"

if not QDRANT_URL or not QDRANT_API_KEY:
    raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables must be set")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable must be set")

qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)


def embed_query(text: str) -> list[float]:
    """Create embeddings for a query using OpenAI text-embedding-3-small."""
    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding


def retrieve(query: str, top_k: int = 5) -> list[dict]:
    """
    Search Qdrant for the top k relevant chunks.

    Args:
        query: The search query text
        top_k: Number of results to return (default: 5)

    Returns:
        List of dicts containing 'text', 'score', and 'metadata' for each result
    """
    query_embedding = embed_query(query)

    results = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=top_k
    )

    chunks = []
    for result in results:
        chunk = {
            "text": result.payload.get("text", ""),
            "score": result.score,
            "metadata": {
                key: value
                for key, value in result.payload.items()
                if key != "text"
            }
        }
        chunks.append(chunk)

    return chunks
