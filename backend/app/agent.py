import os
from typing import AsyncGenerator
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable must be set")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

MODEL = "gpt-4-turbo"

SYSTEM_PROMPT = """You are an expert AI assistant for the Physical AI textbook. Answer questions based on provided context.

Guidelines:
- Provide accurate, detailed answers based on the context provided
- If the context doesn't contain enough information, acknowledge this clearly
- Use clear explanations suitable for students learning about Physical AI
- Reference specific parts of the context when relevant
- Be concise but thorough"""


def format_context(retrieved_chunks: list[dict], selected_text: str | None = None) -> str:
    """
    Format context for the AI, prioritizing user-selected text.

    Args:
        retrieved_chunks: List of chunks from RAG retrieval
        selected_text: Optional user-selected text to prioritize

    Returns:
        Formatted context string
    """
    context_parts = []

    if selected_text:
        context_parts.append(f"**User Selected Text (Primary Focus):**\n{selected_text}")
        context_parts.append("\n---\n")

    if retrieved_chunks:
        context_parts.append("**Relevant Context from Textbook:**\n")
        for i, chunk in enumerate(retrieved_chunks, 1):
            source = chunk.get("metadata", {}).get("source", "Unknown")
            context_parts.append(f"\n[{i}] (Source: {source})\n{chunk['text']}")

    return "\n".join(context_parts) if context_parts else "No context available."


async def stream_response(
    query: str,
    retrieved_chunks: list[dict],
    selected_text: str | None = None,
    conversation_history: list[dict] | None = None
) -> AsyncGenerator[str, None]:
    """
    Stream AI response using GPT-4 Turbo.

    Args:
        query: User's question
        retrieved_chunks: Context chunks from RAG
        selected_text: Optional user-selected text to prioritize
        conversation_history: Optional previous messages for context

    Yields:
        Streamed response chunks
    """
    context = format_context(retrieved_chunks, selected_text)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if conversation_history:
        messages.extend(conversation_history)

    user_message = f"""Context:
{context}

Question: {query}"""

    messages.append({"role": "user", "content": user_message})

    stream = await client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=True,
        temperature=0.7,
        max_tokens=2048
    )

    async for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
