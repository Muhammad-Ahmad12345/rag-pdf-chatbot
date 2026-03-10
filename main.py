from fastapi import FastAPI, UploadFile, File
import shutil
import os

from pdf_processor import extract_text_from_pdf, chunk_text
from chroma_store import store_chunks
from rag_engine import ask_question

app = FastAPI()

UPLOAD_DIR = "data"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pages = extract_text_from_pdf(file_path)

    all_chunks = []

    for page in pages:
        chunks = chunk_text(page["text"])
        all_chunks.extend(chunks)

    total = store_chunks(all_chunks)

    return {
        "message": "Document processed",
        "chunks": total
    }

@app.post("/ask")
def ask(data: dict):
    question = data["question"]
    answer = ask_question(question)
    return {
        "answer": answer
    }

