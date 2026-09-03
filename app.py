from pathlib import Path

from src.document_loader import extract_text_from_pdf
from src.embedding_model import EmbeddingModel
from src.rag_generator import RAGGenerator
from src.text_chunker import chunk_text
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

    # 3. Modelo de embeddings
    print("\nLoading embedding model...")
    embedding_model = EmbeddingModel()

    # 4. Embeddings
    document_embeddings = embedding_model.encode_documents(chunks)

    print(f"Embeddings created: {document_embeddings.shape}")

    # 5. Vector Store
    vector_store = VectorStore()

    vector_store.upsert_chunks(
        chunks=chunks,
        embeddings=document_embeddings,
        source=source,
    )

    print(f"Vectors stored: {vector_store.count()}")

    # 6. Pregunta del usuario
    query = "¿Cuánto tarda el proveedor en entregar?"

    print(f"\nQuestion: {query}")

    # 7. Embedding de la pregunta
    query_embedding = embedding_model.encode_query(query)

    # 8. Recuperar contexto desde ChromaDB
    results = vector_store.search(
        query_embedding=query_embedding,
        top_k=3,
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    contexts = []

    for document, metadata in zip(
        documents,
        metadatas,
    ):
        contexts.append(
            {
                "text": document,
                "source": metadata["source"],
                "chunk_index": metadata["chunk_index"],
            }
        )

    # 9. Generar respuesta con LLM local
    print("\nGenerating RAG answer with Ollama...\n")

    rag_generator = RAGGenerator()

    answer = rag_generator.generate_answer(
        question=query,
        contexts=contexts,
    )

    print("=" * 60)
    print("ANSWER")
    print("=" * 60)
    print(answer)


if __name__ == "__main__":
    main()