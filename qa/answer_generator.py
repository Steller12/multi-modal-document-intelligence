import requests


def build_prompt(question, retrieved_chunks):
    """
    Build a grounded prompt using retrieved context.
    """
    context = ""
    for i, chunk in enumerate(retrieved_chunks, 1):
        context += f"[Source {i} | Page {chunk['page']} | {chunk['modality']}]\n"
        context += chunk["content"] + "\n\n"

    prompt = f"""
You are a factual assistant.
Answer the question using ONLY the sources below.
If the answer is not contained in the sources, say "I don't know".

Question:
{question}

Sources:
{context}

Answer (cite sources like [Source 1]):
"""
    return prompt


def generate_answer(question, retrieved_chunks):
    """
    Generate answer using a local Ollama LLM.
    """
    prompt = build_prompt(question, retrieved_chunks)

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        },
        timeout=300
    )

    response.raise_for_status()
    return response.json()["response"]
