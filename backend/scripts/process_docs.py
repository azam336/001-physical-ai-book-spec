#!/usr/bin/env python3
"""
Process markdown documents for RAG:
1. Chunk documents into smaller pieces
2. Create embeddings using OpenAI
3. Upload to Qdrant vector database
"""

import os
import sys
import re
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# Configuration
DOCS_DIR = Path(__file__).parent.parent.parent / "docs"
COLLECTION_NAME = "001-physical-ai-book-spec"
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSION = 1536
CHUNK_SIZE = 1000  # characters
CHUNK_OVERLAP = 200  # characters

# Initialize clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)


def find_markdown_files(docs_dir: Path) -> list[Path]:
    """Recursively find all markdown files."""
    md_files = []
    for pattern in ["**/*.md", "**/*.mdx"]:
        md_files.extend(docs_dir.glob(pattern))
    return sorted(md_files)


def extract_title(content: str, filepath: Path) -> str:
    """Extract title from markdown content or filename."""
    # Try to find h1 header
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()

    # Try frontmatter title
    match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()

    # Fallback to filename
    return filepath.stem.replace('-', ' ').replace('_', ' ').title()


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks."""
    # Clean the text
    text = re.sub(r'\n{3,}', '\n\n', text)

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # Try to break at paragraph boundary
        if end < len(text):
            # Look for paragraph break
            break_point = text.rfind('\n\n', start, end)
            if break_point > start + chunk_size // 2:
                end = break_point
            else:
                # Look for sentence break
                for sep in ['. ', '! ', '? ', '\n']:
                    break_point = text.rfind(sep, start, end)
                    if break_point > start + chunk_size // 2:
                        end = break_point + len(sep)
                        break

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end - overlap
        if start < 0:
            start = 0

    return chunks


def create_embedding(text: str) -> list[float]:
    """Create embedding using OpenAI."""
    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding


def setup_collection():
    """Create or recreate Qdrant collection."""
    collections = qdrant_client.get_collections().collections
    collection_names = [c.name for c in collections]

    if COLLECTION_NAME in collection_names:
        print(f"Deleting existing collection '{COLLECTION_NAME}'...")
        qdrant_client.delete_collection(COLLECTION_NAME)

    print(f"Creating collection '{COLLECTION_NAME}'...")
    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=EMBEDDING_DIMENSION,
            distance=Distance.COSINE
        )
    )


def process_document(filepath: Path, docs_dir: Path) -> list[dict]:
    """Process a single document into chunks with metadata."""
    print(f"  Processing: {filepath.relative_to(docs_dir)}")

    content = filepath.read_text(encoding='utf-8')
    title = extract_title(content, filepath)
    relative_path = str(filepath.relative_to(docs_dir))

    # Remove frontmatter
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

    chunks = chunk_text(content)

    documents = []
    for i, chunk in enumerate(chunks):
        documents.append({
            "id": str(uuid4()),
            "text": chunk,
            "metadata": {
                "source": relative_path,
                "title": title,
                "chunk_index": i,
                "total_chunks": len(chunks)
            }
        })

    return documents


def upload_to_qdrant(documents: list[dict], batch_size: int = 100):
    """Upload documents to Qdrant with embeddings."""
    print(f"\nUploading {len(documents)} chunks to Qdrant...")

    points = []
    for i, doc in enumerate(documents):
        if (i + 1) % 10 == 0:
            print(f"  Creating embeddings: {i + 1}/{len(documents)}")

        embedding = create_embedding(doc["text"])

        points.append(PointStruct(
            id=doc["id"],
            vector=embedding,
            payload={
                "text": doc["text"],
                **doc["metadata"]
            }
        ))

        # Upload in batches
        if len(points) >= batch_size:
            qdrant_client.upsert(
                collection_name=COLLECTION_NAME,
                points=points
            )
            points = []

    # Upload remaining points
    if points:
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )

    print(f"  Uploaded all chunks successfully!")


def verify_collection():
    """Verify the collection was created correctly."""
    info = qdrant_client.get_collection(COLLECTION_NAME)
    print(f"\nCollection info:")
    print(f"  - Vectors count: {info.vectors_count}")
    print(f"  - Points count: {info.points_count}")


def main():
    print("=" * 50)
    print("Physical AI Book - Document Processing")
    print("=" * 50)

    # Find documents
    print(f"\nSearching for markdown files in: {DOCS_DIR}")
    md_files = find_markdown_files(DOCS_DIR)
    print(f"Found {len(md_files)} markdown files")

    if not md_files:
        print("No markdown files found!")
        sys.exit(1)

    # Setup Qdrant collection
    setup_collection()

    # Process all documents
    print("\nProcessing documents...")
    all_documents = []
    for filepath in md_files:
        docs = process_document(filepath, DOCS_DIR)
        all_documents.extend(docs)

    print(f"\nTotal chunks created: {len(all_documents)}")

    # Upload to Qdrant
    upload_to_qdrant(all_documents)

    # Verify
    verify_collection()

    print("\n" + "=" * 50)
    print("Document processing complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
