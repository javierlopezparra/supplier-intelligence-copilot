import numpy as np


def semantic_search(
    query_embedding,
    document_embeddings,
    chunks: list[str],
    top_k: int = 3,
):
    scores = document_embeddings @ query_embedding

    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for index in top_indices:
        results.append(
            {
                "chunk": chunks[index],
                "score": float(scores[index]),
            }
        )

    return results