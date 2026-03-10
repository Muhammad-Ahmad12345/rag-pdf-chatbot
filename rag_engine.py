from chroma_store import search_chunks
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_question(question):

    results = search_chunks(question)

    chunks = results["documents"][0]
    pages = results["metadatas"][0]

    context = "\n\n".join(chunks)

    prompt = f"""
Answer using only the context below.
If answer not found say 'Not found in document'.

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content

    sources = list(set([p["page"] for p in pages]))

    return answer, sources