import streamlit as st
import requests

API_URL = "https://rag-pdf-chatbot-i42b.onrender.com"

st.title("📄 RAG PDF Chatbot")

st.write("Upload a PDF and ask questions about the document.")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:

    files = {"file": uploaded_file}

    with st.spinner("Processing document..."):

        response = requests.post(
            f"{API_URL}/upload",
            files=files
        )

        st.success(response.json()["message"])
        st.write(f"Chunks created: {response.json()['chunks']}")

question = st.text_input("Ask a question about the document")

if st.button("Ask"):

    if question:

        with st.spinner("Searching document..."):

            response = requests.post(
                f"{API_URL}/ask",
                json={"question": question}
            )

            result = response.json()

            st.subheader("Answer")
            st.write(result["answer"])

            st.subheader("Sources (Page Numbers)")
            st.write(result["sources"])