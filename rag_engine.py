from chroma_store import search_chunks
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(question, chunks):

    context = "\n\n".join(chunks)

    prompt = f"""
You are a helpful assistant.

Use ONLY the context below to answer the question.

If the answer is partially available, provide the best possible answer using the context.

Context:
{context}

Question:
{question}

Answer clearly using the document.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content