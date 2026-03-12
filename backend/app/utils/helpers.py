import hashlib
import uuid
from typing import List


def generate_id() -> str:
    return str(uuid.uuid4())


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks if chunks else [text]


def hash_content(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()
