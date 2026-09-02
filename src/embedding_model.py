from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


class EmbeddingModel:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)

    def encode_documents(self, documents: list[str]):
        return self.model.encode(
            documents,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

    def encode_query(self, query: str):
        return self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )[0]