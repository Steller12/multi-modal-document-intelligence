import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash-lite"
)

def generate_answer(question, retrieved_chunks, doc_keywords=None):
    """
    Generate a grounded answer using Gemini Flash Lite.
    Works for any document type (general-purpose RAG).
    """

    if not retrieved_chunks:
        return "I don't know based on the provided document."

    context_blocks = []

    for i, chunk in enumerate(retrieved_chunks, 1):
        context_blocks.append(
            f"[Source {i} | Page {chunk['page']} | {chunk['modality']}]\n"
            f"{chunk['content']}"
        )

    context = "\n\n".join(context_blocks)

    prompt = f"""
You are a document-grounded assistant.

Answer the user's question using ONLY the sources below.
Do NOT use outside knowledge.

Rules:
- If the sources contain tables, figures, or numeric values,
  summarize overall patterns or trends in words.
- If the sources provide partial or indirect information,
  generate a cautious, high-level answer explaining what can
  reasonably be inferred.
- Use uncertainty-aware language (e.g., "the document suggests",
  "based on available information").
- Do NOT invent facts or numbers.
- Do NOT refuse unless the sources are completely unrelated.

Question:
{question}

Sources:
{context}

Answer:
"""

    try:
        response = model.generate_content(prompt)
        answer = response.text.strip()

        if not answer:
            return "I don't know based on the provided document."

        return answer

    except Exception as e:
        return f"Error generating answer: {e}"
