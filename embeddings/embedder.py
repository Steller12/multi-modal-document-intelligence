from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    """
    Wrapper around a sentence-transformer embedding model.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts):
        """
        Embed a list of texts into dense vectors.
        """
        return self.model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

    def embed_query(self, query: str):
        """
        Embed a single query string.
        """
        return self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
