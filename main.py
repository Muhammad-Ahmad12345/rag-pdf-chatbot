from fastapi import FastAPI, UploadFile, File
import shutil
import os

from pdf_processor import extract_text_from_pdf, chunk_text
from chroma_store import store_chunks, search_chunks, reset_collection
from rag_engine import generate_answer

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    reset_collection()

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pages = extract_text_from_pdf(file_path)

    all_chunks = []
    all_pages = []

    for p in pages:

        chunks = chunk_text(p["text"])

        for c in chunks:
            all_chunks.append(c)
            all_pages.append(p["page"])

    total = store_chunks(all_chunks, all_pages)

    return {
        "message": "Document processed",
        "chunks": total
    }


@app.post("/ask")
async def ask_question(data: dict):

    question = data["question"]

    results = search_chunks(question)

    if not results["documents"] or len(results["documents"][0]) == 0:
        return {
            "answer": "No relevant information found. Please upload document again.",
            "sources": []
        }

    chunks = results["documents"][0]
    pages = [m["page"] for m in results["metadatas"][0]]

    answer = generate_answer(question, chunks)

    return {
        "answer": answer,
        "sources": pages
    }
