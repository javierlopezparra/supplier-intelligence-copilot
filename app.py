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

    data_path = Path("data/raw")
    pdf_files = sorted(data_path.glob("*.pdf"))

    if not pdf_files:
        print("\nNo se encontraron documentos PDF en data/raw/")
        return

    print(f"\nDocumentos encontrados: {len(pdf_files)}")

    # 1. Cargar modelo de embeddings una sola vez
    print("\nLoading embedding model...")
    embedding_model = EmbeddingModel()

    # 2. Inicializar Vector Store
    vector_store = VectorStore()

    # 3. Procesar todos los PDFs
    for pdf_path in pdf_files:
        source = pdf_path.name

        print("\n" + "-" * 60)
        print(f"Procesando: {source}")

        text = extract_text_from_pdf(str(pdf_path))

        chunks = chunk_text(
            text=text,
            chunk_size=700,
            overlap=100,
        )

        print(f"Chunks created: {len(chunks)}")

        document_embeddings = embedding_model.encode_documents(chunks)

        vector_store.upsert_chunks(
            chunks=chunks,
            embeddings=document_embeddings,
            source=source,
        )

    print("\n" + "=" * 60)
    print(f"Vectors stored: {vector_store.count()}")
    print("=" * 60)

    # 4. Iniciar LLM local
    rag_generator = RAGGenerator()

    print("\nCOPILOT READY")
    print("Puedes preguntar o comparar proveedores.")
    print("Escribe 'salir' para terminar.\n")

    # 5. Sesión interactiva
    while True:
        query = input("Pregunta > ").strip()

        if not query:
            continue

        if query.lower() in {"salir", "exit", "quit"}:
            print("\nSesión finalizada.")
            break

        # 6. Crear embedding de la pregunta
        query_embedding = embedding_model.encode_query(query)

        # 7. Recuperar contexto relevante
        results = vector_store.search(
            query_embedding=query_embedding,
            top_k=min(6, vector_store.count()),
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

        # 8. Generar respuesta con el LLM
        answer = rag_generator.generate_answer(
            question=query,
            contexts=contexts,
        )

        print("\nRespuesta:")
        print(answer)
        print()


if __name__ == "__main__":
    main()