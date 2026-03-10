from chroma_store import search_chunks


def ask_question(question):

    chunks = search_chunks(question)

    context = "\n\n".join(chunks)

    answer = f"""
Simulated RAG Answer

Question:
{question}

Context used:
{context[:500]}

(Note: GPT not connected yet)
"""

    return answer