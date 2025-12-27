import faiss
import numpy as np


class VectorStore:

    def __init__(self, embedding_dim: int):
        self.index = faiss.IndexFlatIP(embedding_dim)
        self.metadata = []

    def add(self, vectors, metadata):
        vectors = np.asarray(vectors).astype("float32")
        self.index.add(vectors)
        self.metadata.extend(metadata)

    def search(self, query_vector, top_k: int = 5):
        query_vector = np.asarray([query_vector]).astype("float32")
        scores, indices = self.index.search(query_vector, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])

        return results
