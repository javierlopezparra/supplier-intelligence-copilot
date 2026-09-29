from hashlib import sha256
from pathlib import Path

from src.document_loader import extract_text_from_pdf
from src.embedding_model import EmbeddingModel
from src.rag_generator import RAGGenerator
from src.ranking_explainer import RankingExplainer
from src.supplier_evaluator import SupplierEvaluator
from src.text_chunker import chunk_text
from src.vector_store import VectorStore


def calculate_file_hash(
    file_path: Path,
) -> str:
    hash_object = sha256()

    with open(file_path, "rb") as file:
        for block in iter(
            lambda: file.read(8192),
            b"",
        ):
            hash_object.update(block)

    return hash_object.hexdigest()


def show_ranking(
    ranking: list[dict],
):
    print("\n" + "=" * 60)
    print("RANKING DE PROVEEDORES")
    print("=" * 60)

    for position, supplier in enumerate(
        ranking,
        start=1,
    ):
        print()

        print(
            f"{position}. {supplier['name']} "
            f"→ {supplier['final_score']} puntos"
        )

        print(
            f"   Tiempo de entrega: "
            f"{supplier['lead_time_days']} días"
        )

        print(
            f"   Capacidad mensual: "
            f"{supplier['monthly_capacity']:,} unidades"
        )

        print(
            f"   Condiciones de pago: "
            f"{supplier['payment_terms_days']} días"
        )

    print()


def main():
    print("=" * 60)
    print("SUPPLIER INTELLIGENCE COPILOT")
    print("=" * 60)

    data_path = Path("data/raw")
    pdf_files = sorted(
        data_path.glob("*.pdf")
    )

    if not pdf_files:
        print(
            "\nNo se encontraron documentos PDF "
            "en data/raw/"
        )
        return

    print(
        f"\nDocumentos encontrados: "
        f"{len(pdf_files)}"
    )

    # 1. Cargar modelo de embeddings
    print("\nLoading embedding model...")

    embedding_model = EmbeddingModel()

    # 2. Inicializar base vectorial
    vector_store = VectorStore()

    # 3. Eliminar del índice documentos
    # que ya no existen en data/raw
    current_sources = {
        pdf_path.name
        for pdf_path in pdf_files
    }

    removed_sources = (
        vector_store.delete_missing_sources(
            current_sources
        )
    )

    if removed_sources:
        print("\nDocumentos eliminados del índice:")

        for source in removed_sources:
            print(f"- {source}")

    indexed_documents = 0
    reused_documents = 0

    # 4. Revisar todos los PDFs
    for pdf_path in pdf_files:
        source = pdf_path.name

        print("\n" + "-" * 60)
        print(f"Revisando: {source}")

        document_hash = calculate_file_hash(
            pdf_path
        )

        needs_indexing = (
            vector_store.source_needs_indexing(
                source=source,
                document_hash=document_hash,
            )
        )

        if not needs_indexing:
            print(
                "Sin cambios. "
                "Se reutiliza el índice existente."
            )

            reused_documents += 1
            continue

        print(
            "Documento nuevo o modificado. "
            "Procesando..."
        )

        text = extract_text_from_pdf(
            str(pdf_path)
        )

        chunks = chunk_text(
            text=text,
            chunk_size=700,
            overlap=100,
        )

        print(
            f"Chunks created: {len(chunks)}"
        )

        document_embeddings = (
            embedding_model.encode_documents(
                chunks
            )
        )

        vector_store.upsert_chunks(
            chunks=chunks,
            embeddings=document_embeddings,
            source=source,
            document_hash=document_hash,
        )

        indexed_documents += 1

    print("\n" + "=" * 60)
    print(
        f"Vectors stored: "
        f"{vector_store.count()}"
    )

    print(
        f"Documentos indexados: "
        f"{indexed_documents}"
    )

    print(
        f"Documentos reutilizados: "
        f"{reused_documents}"
    )

    print("=" * 60)

    # 5. Inicializar RAG
    rag_generator = RAGGenerator()

    # 6. Inicializar evaluación
    evaluator = SupplierEvaluator()

    suppliers = evaluator.load_suppliers()

    ranking = evaluator.evaluate(
        suppliers
    )

    # 7. Inicializar explicación con IA
    ranking_explainer = RankingExplainer()

    print("\nCOPILOT READY")
    print()
    print("Puedes:")
    print(
        "- Hacer preguntas sobre "
        "los proveedores."
    )
    print(
        "- Escribir 'ranking' para "
        "ver la evaluación."
    )
    print(
        "- Escribir 'explicar ranking' "
        "para obtener el análisis con IA."
    )
    print(
        "- Escribir 'salir' para terminar."
    )
    print()

    # 8. Sesión interactiva
    while True:
        query = input(
            "Pregunta > "
        ).strip()

        if not query:
            continue

        command = query.lower()

        if command in {
            "salir",
            "exit",
            "quit",
        }:
            print(
                "\nSesión finalizada."
            )
            break

        if command == "ranking":
            show_ranking(ranking)
            continue

        if command in {
            "explicar ranking",
            "explica ranking",
            "analizar ranking",
        }:
            print(
                "\nGenerando explicación "
                "del ranking...\n"
            )

            explanation = (
                ranking_explainer.explain(
                    ranking=ranking,
                    weights=evaluator.weights,
                )
            )

            print("=" * 60)
            print(
                "EXPLICACIÓN DEL RANKING"
            )
            print("=" * 60)
            print()
            print(explanation)
            print()

            continue

        # 9. Pregunta documental con RAG
        query_embedding = (
            embedding_model.encode_query(
                query
            )
        )

        results = vector_store.search(
            query_embedding=query_embedding,
            top_k=min(
                6,
                vector_store.count(),
            ),
        )

        documents = (
            results["documents"][0]
        )

        metadatas = (
            results["metadatas"][0]
        )

        contexts = []

        for document, metadata in zip(
            documents,
            metadatas,
        ):
            contexts.append(
                {
                    "text": document,
                    "source":
                        metadata["source"],
                    "chunk_index":
                        metadata["chunk_index"],
                }
            )

        answer = (
            rag_generator.generate_answer(
                question=query,
                contexts=contexts,
            )
        )

        print("\nRespuesta:")
        print(answer)
        print()


if __name__ == "__main__":
    main()