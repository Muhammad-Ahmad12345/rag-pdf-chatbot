import streamlit as st
import requests
import time

API_URL = "https://rag-pdf-chatbot-i42b.onrender.com"

st.title("📄 RAG PDF Chatbot")
st.write("Upload a PDF and ask questions about the document.")

def safe_post(url, **kwargs):
    for i in range(6):  # retry 6 times
        try:
            response = requests.post(url, timeout=60, **kwargs)
            if response.status_code == 200:
                return response
        except:
            pass

        time.sleep(3)

    return None


try:
    requests.get(API_URL, timeout=10)
except:
    pass

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:

    with st.spinner("Processing document..."):

        response = safe_post(
            f"{API_URL}/upload",
            files={"file": uploaded_file}
        )

        if response:
            data = response.json()
            st.success(data["message"])
            st.write(f"Chunks created: {data['chunks']}")
        else:
            st.error("Server is starting, please try again.")

question = st.text_input("Ask a question about the document")

if st.button("Ask"):

    if question:

        with st.spinner("Searching document..."):

            response = safe_post(
                f"{API_URL}/ask",
                json={"question": question}
            )

            if response:
                result = response.json()

                st.subheader("Answer")
                st.write(result["answer"])

                st.subheader("Sources (Page Numbers)")
                st.write(result["sources"])
            else:
                st.error("Server not ready yet. Try again.")