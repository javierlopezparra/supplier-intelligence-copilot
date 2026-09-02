from pathlib import Path

from src.document_loader import extract_text_from_pdf
from src.text_chunker import chunk_text
from src.embedding_model import EmbeddingModel
from src.vector_store import VectorStore


def main():
    print("=" * 60)
    print("SUPPLIER INTELLIGENCE COPILOT")
    print("=" * 60)

    pdf_path = "data/raw/sample_supplier.pdf"
    source = Path(pdf_path).name

    # 1. Leer documento
    text = extract_text_from_pdf(pdf_path)
    print("\nDocument loaded successfully.")

    # 2. Crear chunks
    chunks = chunk_text(
        text=text,
        chunk_size=180,
        overlap=40,
    )

    print(f"Total chunks created: {len(chunks)}")

    # 3. Cargar modelo de embeddings
    print("\nLoading embedding model...")
    embedding_model = EmbeddingModel()

    # 4. Crear embeddings
    document_embeddings = embedding_model.encode_documents(chunks)

    print(f"Embeddings created: {document_embeddings.shape}")

    # 5. Inicializar ChromaDB
    vector_store = VectorStore()

    # 6. Guardar chunks y embeddings
    vector_store.upsert_chunks(
        chunks=chunks,
        embeddings=document_embeddings,
        source=source,
    )

    print(f"\nVectors stored: {vector_store.count()}")

    # 7. Pregunta
    query = "¿Cuánto tarda el proveedor en entregar?"

    print(f"\nQuestion: {query}")

    # 8. Crear embedding de la pregunta
    query_embedding = embedding_model.encode_query(query)

    # 9. Buscar en Vector Store
    results = vector_store.search(
        query_embedding=query_embedding,
        top_k=3,
    )

    print("\nMost relevant chunks:")

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for position, (document, metadata, distance) in enumerate(
        zip(documents, metadatas, distances),
        start=1,
    ):
        print("\n" + "-" * 60)

        print(
            f"RESULT {position} | "
            f"Distance: {distance:.4f}"
        )

        print(
            f"Source: {metadata['source']} | "
            f"Chunk: {metadata['chunk_index']}"
        )

        print("-" * 60)
        print(document)


if __name__ == "__main__":
    main()