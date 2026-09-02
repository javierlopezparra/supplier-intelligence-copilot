from pathlib import Path

import chromadb


class VectorStore:
    def __init__(
        self,
        path: str = "data/vector_store",
        collection_name: str = "supplier_documents",
    ):
        Path(path).mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(path=path)

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def upsert_chunks(
        self,
        chunks: list[str],
        embeddings,
        source: str,
    ):
        ids = [
            f"{source}-chunk-{index}"
            for index in range(len(chunks))
        ]

        metadatas = [
            {
                "source": source,
                "chunk_index": index,
            }
            for index in range(len(chunks))
        ]

        self.collection.upsert(
            ids=ids,
            documents=chunks,
            embeddings=embeddings.tolist(),
            metadatas=metadatas,
        )

    def search(
        self,
        query_embedding,
        top_k: int = 3,
    ):
        return self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

    def count(self) -> int:
        return self.collection.count()