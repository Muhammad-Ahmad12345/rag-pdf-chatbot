import chromadb
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(name="rag_collection")


def reset_collection():
    global collection
    chroma_client.delete_collection("rag_collection")
    collection = chroma_client.create_collection("rag_collection")


def store_chunks(chunks, pages):

    ids = []
    embeddings = []

    for i, chunk in enumerate(chunks):

        emb = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk
        )

        embeddings.append(emb.data[0].embedding)
        ids.append(str(i))

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=[{"page": p} for p in pages]
    )

    return len(chunks)


def search_chunks(query):

    emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )

    query_embedding = emb.data[0].embedding

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    return results