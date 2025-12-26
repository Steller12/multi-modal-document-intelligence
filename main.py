import os

from ingestion.pipeline import ingest_document
from chunking.chunker import chunk_records
from embeddings.embedder import EmbeddingModel
from retrieval.vector_store import VectorStore
from retrieval.retriever import Retriever
from qa.answer_generator import generate_answer


# set paths
base_dir = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(base_dir, "data", "qatar_test_doc.pdf")


# ingest document
print("\n[1] ingesting document...")
records = ingest_document(pdf_path)
print(f"extracted {len(records)} records")


# chunk content
print("\n[2] chunking records...")
chunks = chunk_records(records)
print(f"created {len(chunks)} chunks")


# generate embeddings
print("\n[3] generating embeddings...")
embedder = EmbeddingModel()
texts = [c["content"] for c in chunks]
vectors = embedder.embed_texts(texts)
print(f"embeddings shape: {vectors.shape}")


# build vector store
print("\n[4] building vector store...")
store = VectorStore(embedding_dim=vectors.shape[1])
store.add(vectors, chunks)
retriever = Retriever(embedder, store)
print("vector store ready")


# test question
question = "what does the document say about economic growth and outlook?"


# retrieve context
print("\n[5] retrieving relevant context...")
retrieved_chunks = retriever.retrieve(question, top_k=3)

for i, chunk in enumerate(retrieved_chunks, 1):
    print(f"\n--- source {i} | page {chunk['page']} | {chunk['modality']} ---")
    print(chunk["content"][:300])


# generate answer
print("\n[6] generating answer...\n")
answer = generate_answer(question, retrieved_chunks)

print("question:")
print(question)

print("\nanswer:")
print(answer)
