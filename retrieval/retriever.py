class Retriever:

    def __init__(self, embedder, vector_store):
        self.embedder = embedder
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 5):
        query_vector = self.embedder.embed_query(query)

        candidates = self.vector_store.search(query_vector, top_k=top_k * 4)

        text_chunks = [c for c in candidates if c["modality"] == "text"]
        table_chunks = [c for c in candidates if c["modality"] == "table"]
        image_chunks = [c for c in candidates if c["modality"] == "image"]

        results = []

        results.extend(text_chunks[:top_k])

        if any(k in query.lower() for k in ["gdp", "growth", "inflation", "percent", "rate"]):
            if len(results) < top_k:
                results.extend(table_chunks[: top_k - len(results)])

        elif len(results) < top_k:
            results.extend(table_chunks[: top_k - len(results)])

        return results[:top_k]
