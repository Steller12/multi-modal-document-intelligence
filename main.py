# main.py
import os

from ingestion.pipeline import ingest_document
from chunking.chunker import chunk_records
from embeddings.embedder import EmbeddingModel
from retrieval.vector_store import VectorStore
from retrieval.retriever import Retriever
from qa.answer_generator import generate_answer

# --------------------------------------------------
# 1. Path setup
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(BASE_DIR, "data", "qatar_test_doc.pdf")

# --------------------------------------------------
# 2. Ingest document (Day 1)
# --------------------------------------------------
print("\n[1] Ingesting document...")
records = ingest_document(PDF_PATH)
print(f"Extracted {len(records)} records")

# --------------------------------------------------
# 3. Chunk records (Day 2 - Step 1)
# --------------------------------------------------
print("\n[2] Chunking records...")
chunks = chunk_records(records)
print(f"Created {len(chunks)} chunks")

# --------------------------------------------------
# 4. Embed chunks (Day 2 - Step 2)
# --------------------------------------------------
print("\n[3] Generating embeddings...")
embedder = EmbeddingModel()
texts = [c["content"] for c in chunks]
vectors = embedder.embed_texts(texts)
print(f"Generated embeddings with shape {vectors.shape}")

# --------------------------------------------------
# 5. Build vector store (Day 2 - Step 3)
# --------------------------------------------------
print("\n[4] Building vector store...")
store = VectorStore(embedding_dim=vectors.shape[1])
store.add(vectors, chunks)
retriever = Retriever(embedder, store)
print("Vector store ready")

# --------------------------------------------------
# 6. Ask a test question (Day 3 - OpenAI QA)
# --------------------------------------------------
question = "What is Qatar's economic outlook and GDP growth?"

print("\n[5] Retrieving relevant context...")
retrieved_chunks = retriever.retrieve(question, top_k=3)

for i, chunk in enumerate(retrieved_chunks, 1):
    print(f"\n--- Source {i} | Page {chunk['page']} | {chunk['modality']} ---")
    print(chunk["content"][:300])

# --------------------------------------------------
# 7. Generate answer using OpenAI
# --------------------------------------------------
print("\n[6] Generating answer with OpenAI...\n")
answer = generate_answer(question, retrieved_chunks)

print("QUESTION:")
print(question)

print("\nANSWER:")
print(answer)
