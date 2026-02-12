"""
Ingestion pipeline: reads book markdown, chunks, embeds, and upserts to Qdrant.
Usage: python ingest.py
"""

import uuid
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from config import (
    OPENAI_API_KEY,
    QDRANT_URL,
    QDRANT_COLLECTION,
    EMBEDDING_MODEL,
    EMBEDDING_DIMENSIONS,
    DOCS_DIR,
)
from chunker import get_all_chunks

BATCH_SIZE = 20


def make_id(source_file: str, heading: str) -> str:
    """Generate a deterministic UUID from source file + heading."""
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"{source_file}::{heading}"))


def main():
    print("=== Physical AI Book Ingestion ===\n")

    # 1. Initialize clients
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
    qdrant_client = QdrantClient(url=QDRANT_URL)

    # 2. Get all chunks
    print("Reading and chunking markdown files...")
    chunks = get_all_chunks(str(DOCS_DIR))
    print(f"\nTotal chunks to ingest: {len(chunks)}\n")

    if not chunks:
        print("No chunks found. Check your docs directory.")
        return

    # 3. Recreate Qdrant collection (idempotent)
    print(f"Creating Qdrant collection '{QDRANT_COLLECTION}'...")
    qdrant_client.recreate_collection(
        collection_name=QDRANT_COLLECTION,
        vectors_config=VectorParams(
            size=EMBEDDING_DIMENSIONS,
            distance=Distance.COSINE,
        ),
    )
    print("Collection created.\n")

    # 4. Embed and upsert in batches
    total_upserted = 0
    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i : i + BATCH_SIZE]
        texts = [chunk["text"] for chunk in batch]

        # Generate embeddings
        print(f"Embedding batch {i // BATCH_SIZE + 1} ({len(batch)} chunks)...")
        response = openai_client.embeddings.create(
            input=texts,
            model=EMBEDDING_MODEL,
        )

        # Build Qdrant points
        points = []
        for j, (chunk, embedding_data) in enumerate(zip(batch, response.data)):
            point_id = make_id(
                chunk["metadata"]["source_file"],
                chunk["metadata"]["heading"] or f"intro_{i + j}",
            )
            points.append(
                PointStruct(
                    id=point_id,
                    vector=embedding_data.embedding,
                    payload={
                        "text": chunk["text"],
                        "source_file": chunk["metadata"]["source_file"],
                        "title": chunk["metadata"]["title"],
                        "heading": chunk["metadata"]["heading"],
                    },
                )
            )

        # Upsert to Qdrant
        qdrant_client.upsert(
            collection_name=QDRANT_COLLECTION,
            points=points,
        )
        total_upserted += len(points)
        print(f"  Upserted {total_upserted}/{len(chunks)} points.")

    print(f"\n=== Done! Ingested {total_upserted} chunks into '{QDRANT_COLLECTION}' ===")


if __name__ == "__main__":
    main()
