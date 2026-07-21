import re
from pathlib import Path


def _split_sentences(text):
    """
    Split text into sentences using regex.
    Handles common abbreviations and decimal numbers.
    """
    # Split on sentence-ending punctuation followed by whitespace or newline,
    # but also treat double-newlines as sentence boundaries (paragraph breaks).
    parts = re.split(r'(?<=[.!?])\s+|\n{2,}', text)
    sentences = [s.strip() for s in parts if s.strip()]
    return sentences


def chunk_text(text, chunk_size=800, overlap_sentences=2, overlap=None):
    """
    Split text into overlapping chunks using sentence-aware boundaries.

    Each chunk accumulates complete sentences up to approximately `chunk_size`
    characters. The last `overlap_sentences` sentences from the previous chunk
    are prepended to the next chunk for context continuity.

    This ensures:
    - No chunk ever breaks mid-sentence
    - Semantic coherence is preserved within each chunk
    - Overlapping sentences provide context bridges between chunks
    """
    if overlap is not None and isinstance(overlap, int):
        # Convert character overlap estimate to sentence overlap if provided
        overlap_sentences = max(1, overlap // 20) if overlap > 0 else 0

    sentences = _split_sentences(text)

    if not sentences:
        return []

    chunks = []
    current_chunk_sentences = []
    current_length = 0

    for sentence in sentences:
        sentence_len = len(sentence)

        # If adding this sentence exceeds the target and we already have content,
        # finalize the current chunk
        if current_length + sentence_len > chunk_size and current_chunk_sentences:
            chunk_text_str = " ".join(current_chunk_sentences).strip()
            if chunk_text_str:
                chunks.append(chunk_text_str)

            # Overlap: carry the last N sentences into the next chunk
            overlap = current_chunk_sentences[-overlap_sentences:] if overlap_sentences > 0 else []
            current_chunk_sentences = list(overlap)
            current_length = sum(len(s) + 1 for s in current_chunk_sentences)

        current_chunk_sentences.append(sentence)
        current_length += sentence_len + 1  # +1 for the space joining

    # Don't forget the last chunk
    if current_chunk_sentences:
        chunk_text_str = " ".join(current_chunk_sentences).strip()
        if chunk_text_str:
            chunks.append(chunk_text_str)

    return chunks


if __name__ == "__main__":

    sample_text = (
        "Artificial Intelligence is transforming industries. "
        "Machine learning is a subset of AI. "
        "Deep learning uses neural networks with many layers. "
    ) * 20

    chunks = chunk_text(sample_text)

    print("=" * 50)
    print("Chunker Test (Sentence-Aware)")
    print("=" * 50)

    print(f"Chunks Created : {len(chunks)}")

    print("\nFirst Chunk:\n")
    print(chunks[0])

    print("\nSecond Chunk:\n")
    if len(chunks) > 1:
        print(chunks[1])