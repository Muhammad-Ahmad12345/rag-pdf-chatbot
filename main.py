from fastapi import FastAPI, UploadFile, File
import shutil
import os
from dotenv import load_dotenv

from pdf_processor import extract_text_from_pdf, chunk_text
from chroma_store import store_chunks
from rag_engine import ask_question

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

print("OPENAI_API_KEY:", api_key)  

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
    all_pages = []

    for page in pages:
        chunks = chunk_text(page["text"])
        for c in chunks:
         all_chunks.append(c)
        all_pages.append(page["page"])


    total = store_chunks(all_chunks, all_pages)

    return {
        "message": "Document processed",
        "chunks": total
    }

@app.post("/ask")
def ask(data: dict):

    question = data["question"]

    answer, sources = ask_question(question)

    return {
        "answer": answer,
        "sources": sources
    }
