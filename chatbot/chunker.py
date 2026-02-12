"""
Markdown chunker for the Physical AI book.
Splits markdown files by ## headings into chunks with metadata.
"""

import re
import glob
from pathlib import Path


def _strip_frontmatter(text: str) -> tuple[str, str]:
    """Remove YAML frontmatter and extract the title."""
    title = ""
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if match:
        frontmatter = match.group(1)
        # Extract title from frontmatter
        title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', frontmatter, re.MULTILINE)
        if title_match:
            title = title_match.group(1)
        text = text[match.end():]
    return text, title


def split_markdown_by_headings(file_path: str) -> list[dict]:
    """
    Split a markdown file into chunks at ## headings.
    Returns list of dicts with 'text' and 'metadata' keys.
    """
    path = Path(file_path)
    content = path.read_text(encoding="utf-8")
    content, title = _strip_frontmatter(content)

    source_file = path.name

    # Split on ## headings (keep the heading with the chunk)
    sections = re.split(r"(?=^## )", content, flags=re.MULTILINE)

    chunks = []
    for section in sections:
        section = section.strip()
        if not section or len(section) < 50:
            continue

        # Extract heading if present
        heading = ""
        heading_match = re.match(r"^## (.+)$", section, re.MULTILINE)
        if heading_match:
            heading = heading_match.group(1).strip()

        # Build the text with hierarchical context
        if heading and title:
            chunk_text = f"{title} > {heading}\n\n{section}"
        else:
            chunk_text = f"{title}\n\n{section}" if title else section

        chunks.append({
            "text": chunk_text,
            "metadata": {
                "source_file": source_file,
                "title": title,
                "heading": heading,
            },
        })

    return chunks


def get_all_chunks(docs_dir: str) -> list[dict]:
    """
    Read all markdown files from docs directory and return all chunks.
    """
    docs_path = Path(docs_dir)
    md_files = sorted(docs_path.glob("**/*.md"))

    all_chunks = []
    for md_file in md_files:
        chunks = split_markdown_by_headings(str(md_file))
        all_chunks.extend(chunks)
        print(f"  {md_file.name}: {len(chunks)} chunks")

    return all_chunks


if __name__ == "__main__":
    from config import DOCS_DIR
    chunks = get_all_chunks(str(DOCS_DIR))
    print(f"\nTotal: {len(chunks)} chunks")
    if chunks:
        print(f"\nFirst chunk preview:")
        print(f"  Source: {chunks[0]['metadata']['source_file']}")
        print(f"  Heading: {chunks[0]['metadata']['heading']}")
        print(f"  Text length: {len(chunks[0]['text'])} chars")
