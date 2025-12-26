import faiss
import numpy as np


class VectorStore:
    """
    Simple FAISS-based vector store with metadata tracking.
    """

    def __init__(self, embedding_dim: int):
        self.index = faiss.IndexFlatIP(embedding_dim)
        self.metadata = []

    def add(self, vectors, metadata):
        """
        Add vectors and corresponding metadata to the index.
        """
        vectors = np.asarray(vectors).astype("float32")
        self.index.add(vectors)
        self.metadata.extend(metadata)

    def search(self, query_vector, top_k: int = 5):
        """
        Search the index and return top-k metadata entries.
        """
        query_vector = np.asarray([query_vector]).astype("float32")
        scores, indices = self.index.search(query_vector, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])

        return results
