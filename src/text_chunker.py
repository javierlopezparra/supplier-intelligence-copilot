def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100
) -> list[str]:
    """
    Split text into overlapping chunks without breaking words.

    Args:
        text: Full document text.
        chunk_size: Approximate maximum characters per chunk.
        overlap: Approximate characters repeated between chunks.

    Returns:
        List of text chunks.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap cannot be negative")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    words = text.split()

    chunks = []
    current_words = []
    current_length = 0

    for word in words:
        word_length = len(word) + 1

        if current_length + word_length > chunk_size and current_words:
            chunk = " ".join(current_words)
            chunks.append(chunk)

            overlap_words = []
            overlap_length = 0

            for previous_word in reversed(current_words):
                previous_length = len(previous_word) + 1

                if overlap_length + previous_length > overlap:
                    break

                overlap_words.insert(0, previous_word)
                overlap_length += previous_length

            current_words = overlap_words.copy()
            current_length = overlap_length

        current_words.append(word)
        current_length += word_length

    if current_words:
        chunks.append(" ".join(current_words))

    return chunks