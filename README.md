# Simple Deployable RAG PDF Chatbot

This project implements a simple Retrieval Augmented Generation (RAG) chatbot.

Features:
- Upload PDF documents
- Extract and chunk text
- Store embeddings in Chroma vector database
- Retrieve relevant chunks
- Answer questions based on document context

Tech Stack:
- Python
- FastAPI
- Chroma Vector DB
- Streamlit UI
- Docker

Endpoints:

POST /upload
Upload a PDF document and process it into chunks.

POST /ask
Ask a question about the uploaded document.

Run server:

uvicorn main:app --reload