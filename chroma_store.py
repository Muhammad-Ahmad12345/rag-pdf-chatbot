import chromadb

chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(
    name="pdf_documents"
)


def store_chunks(chunks):

    for i, chunk in enumerate(chunks):

        fake_embedding = [0.1] * 1536

        collection.add(
            documents=[chunk],
            embeddings=[fake_embedding],
            ids=[str(i)]
        )

    return len(chunks)

def search_chunks(question):

    fake_embedding = [0.1] * 1536

    results = collection.query(
        query_embeddings=[fake_embedding],
        n_results=5
    )

    return results["documents"][0]