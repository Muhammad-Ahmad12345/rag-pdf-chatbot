import chromadb
from openai import OpenAI
import os 

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(
    name="pdf_documents"
)


def store_chunks(chunks, pages):

    for i, chunk in enumerate(chunks):

        emb = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk
        )

        embedding = emb.data[0].embedding

        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[str(i)],
            metadatas=[{"page": pages[i]}]
        )

    return len(chunks)


def search_chunks(question):

    emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    )

    query_embedding = emb.data[0].embedding

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    return results