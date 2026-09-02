from src.document_loader import extract_text_from_pdf
from src.text_chunker import chunk_text
from src.embedding_model import EmbeddingModel
from src.semantic_search import semantic_search


def main():
    print("=" * 60)
    print("SUPPLIER INTELLIGENCE COPILOT")
    print("=" * 60)

    pdf_path = "data/raw/sample_supplier.pdf"

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

    # 4. Convertir chunks a vectores
    document_embeddings = embedding_model.encode_documents(chunks)

    print(f"Embeddings created: {document_embeddings.shape}")

    # 5. Pregunta
    query = "¿Cuánto tarda el proveedor en entregar?"

    print(f"\nQuestion: {query}")

    # 6. Convertir pregunta a vector
    query_embedding = embedding_model.encode_query(query)

    # 7. Buscar chunks similares
    results = semantic_search(
        query_embedding=query_embedding,
        document_embeddings=document_embeddings,
        chunks=chunks,
        top_k=3,
    )

    print("\nMost relevant chunks:")

    for position, result in enumerate(results, start=1):
        print("\n" + "-" * 60)
        print(
            f"RESULT {position} | "
            f"Similarity: {result['score']:.4f}"
        )
        print("-" * 60)
        print(result["chunk"])


if __name__ == "__main__":
    main()