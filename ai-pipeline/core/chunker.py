"""
chunker.py
----------
Splits long text into smaller chunks for embeddings, RAG, and flashcard generation.
"""

import logging
from typing import List

import config

logger = logging.getLogger(__name__)


class TextChunker:
    """
    Splits text into overlapping chunks to preserve context.
    """

    def __init__(self, chunk_size: int = 500, overlap: int = 100):
        if overlap >= chunk_size:
            raise ValueError("Overlap must be smaller than chunk_size")
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into chunks of size `chunk_size` with overlap.
        """
        if not text.strip():
            logger.warning("Received empty text for chunking.")
            return []

        words = text.split()
        chunks = []
        start = 0

        while start < len(words):
            end = start + self.chunk_size
            chunk = " ".join(words[start:end])
            chunks.append(chunk)
            start += self.chunk_size - self.overlap

        logger.info(f"Chunked text into {len(chunks)} parts (chunk_size={self.chunk_size}, overlap={self.overlap})")
        return chunks

    def chunk_bulk(self, texts: List[str]) -> List[List[str]]:
        """
        Chunk multiple documents.
        """
        return [self.chunk_text(t) for t in texts]


if __name__ == "__main__":
    sample_text = "This is a sample sentence that will be chunked into overlapping sections." * 20
    chunker = TextChunker()
    chunks = chunker.chunk_text(sample_text)
    print(f"Generated {len(chunks)} chunks.")
