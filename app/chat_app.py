# app/chat_app.py

import sys
import os
import tempfile
from collections import Counter

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

import streamlit as st

from ingestion.pipeline import ingest_document
from chunking.chunker import chunk_records
from embeddings.embedder import EmbeddingModel
from retrieval.vector_store import VectorStore
from retrieval.retriever import Retriever
from qa.answer_generator import generate_answer

st.set_page_config(page_title="RAG Chatbot", layout="wide")
st.title("📄 Multi-Modal Document Intelligence (RAG-Based QA System)")

st.markdown(
    """
Upload **any document** and ask questions about it.
The assistant answers **only using the uploaded document**
"""
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "doc_keywords" not in st.session_state:
    st.session_state.doc_keywords = set()

if "current_file" not in st.session_state:
    st.session_state.current_file = None

def extract_document_keywords(chunks, top_k=15):
    words = []
    for c in chunks:
        words.extend(c["content"].lower().split())

    stopwords = {
        "the", "and", "of", "to", "in", "a", "is", "for", "on",
        "with", "as", "by", "an", "are", "this", "that", "from"
    }

    words = [w for w in words if w.isalpha() and w not in stopwords]
    return set(w for w, _ in Counter(words).most_common(top_k))

def expand_query(question: str):
    q = question.lower()

    if any(k in q for k in ["gdp", "growth", "inflation", "debt", "deficit", "percent"]):
        return question + " table figures data statistics"

    if any(k in q for k in ["summary", "overview", "about"]):
        return question + " introduction background purpose"

    if any(k in q for k in ["outlook", "future", "expect"]):
        return question + " outlook expectations projections"

    if any(k in q for k in ["risk", "challenge", "concern"]):
        return question + " risks challenges uncertainties"

    return question

uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

if uploaded_file:
    if st.session_state.current_file != uploaded_file.name:
        st.session_state.current_file = uploaded_file.name
        st.session_state.chat_history = []
        st.session_state.retriever = None
        st.session_state.doc_keywords = set()

    if st.session_state.retriever is None:
        with st.spinner("Indexing document..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                pdf_path = tmp.name

            records = ingest_document(pdf_path)
            chunks = chunk_records(records)

            embedder = EmbeddingModel()
            embeddings = embedder.embed_texts([c["content"] for c in chunks])

            store = VectorStore(embeddings.shape[1])
            store.add(embeddings, chunks)

            st.session_state.retriever = Retriever(embedder, store)
            st.session_state.doc_keywords = extract_document_keywords(chunks)

        st.success("Document indexed. You can now ask questions.")

if st.session_state.retriever:
    st.subheader("💬 Chat")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_question = st.chat_input("Ask a question about the document")

    if user_question:
        st.session_state.chat_history.append(
            {"role": "user", "content": user_question}
        )
        with st.chat_message("user"):
            st.markdown(user_question)

        with st.spinner("Retrieving and reasoning..."):
            expanded_query = expand_query(user_question)

            retrieved_chunks = st.session_state.retriever.retrieve(
                expanded_query, top_k=3
            )

            answer = generate_answer(
                user_question,
                retrieved_chunks,
                st.session_state.doc_keywords
            )

        st.session_state.chat_history.append(
            {"role": "assistant", "content": answer}
        )
        with st.chat_message("assistant"):
            st.markdown(answer)

        with st.expander("🔍 Retrieved Evidence (Debug)"):
            for c in retrieved_chunks:
                st.write(f"Page {c['page']} | {c['modality']}")
                st.write(c["content"][:400])
                st.write("---")

else:
    st.info("Upload a document to start chatting.")
