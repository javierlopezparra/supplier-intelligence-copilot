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

    def source_needs_indexing(
        self,
        source: str,
        document_hash: str,
    ) -> bool:
        result = self.collection.get(
            where={"source": source},
            include=["metadatas"],
        )

        if not result["ids"]:
            return True

        metadatas = result.get("metadatas") or []

        stored_hashes = {
            metadata.get("document_hash")
            for metadata in metadatas
            if metadata
        }

        return stored_hashes != {document_hash}

    def upsert_chunks(
        self,
        chunks: list[str],
        embeddings,
        source: str,
        document_hash: str,
    ):
        # Eliminar versiones anteriores del documento
        self.delete_source(source)

        ids = [
            f"{source}-chunk-{index}"
            for index in range(len(chunks))
        ]

        metadatas = [
            {
                "source": source,
                "chunk_index": index,
                "document_hash": document_hash,
            }
            for index in range(len(chunks))
        ]

        self.collection.upsert(
            ids=ids,
            documents=chunks,
            embeddings=embeddings.tolist(),
            metadatas=metadatas,
        )

    def delete_source(
        self,
        source: str,
    ):
        self.collection.delete(
            where={"source": source}
        )

    def get_indexed_sources(self) -> set[str]:
        result = self.collection.get(
            include=["metadatas"]
        )

        metadatas = result.get("metadatas") or []

        return {
            metadata["source"]
            for metadata in metadatas
            if metadata and "source" in metadata
        }

    def delete_missing_sources(
        self,
        existing_sources: set[str],
    ) -> list[str]:
        indexed_sources = self.get_indexed_sources()

        missing_sources = (
            indexed_sources - existing_sources
        )

        for source in missing_sources:
            self.delete_source(source)

        return sorted(missing_sources)

    def search(
        self,
        query_embedding,
        top_k: int = 3,
    ):
        return self.collection.query(
            query_embeddings=[
                query_embedding.tolist()
            ],
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

    def count(self) -> int:
        return self.collection.count()