import streamlit as st
import requests
import time

API_URL = "https://rag-pdf-chatbot-i42b.onrender.com"

st.title("📄 RAG PDF Chatbot")

st.write("Upload a PDF and ask questions about the document.")

# 🔥 Retry function (handles cold start)
def call_api(url, method="POST", retries=4, delay=2, **kwargs):

    for i in range(retries):
        try:
            if method == "POST":
                response = requests.post(url, timeout=60, **kwargs)
            else:
                response = requests.get(url, timeout=60)

            if response.status_code == 200:
                return response

        except:
            pass

        time.sleep(delay)

    return None


# 🔥 Silent warmup (only first time)
if "warmed_up" not in st.session_state:

    with st.spinner("Preparing system..."):
        call_api(API_URL, method="GET")

    st.session_state["warmed_up"] = True


# 📂 Upload section
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:

    with st.spinner("Processing thedocument..."):

        response = call_api(
            f"{API_URL}/upload",
            files={"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        )

        if response:

            data = response.json()

            st.success(data.get("message", "Document processed"))
            st.write(f"Chunks created: {data.get('chunks', 0)}")

        else:
            st.error("System is starting. Please try again.")


# ❓ Ask question section
question = st.text_input("Ask a question about the document")

if st.button("Ask"):

    if question:

        with st.spinner("Finding answer from document..."):

            response = call_api(
                f"{API_URL}/ask",
                json={"question": question}
            )

            if response:

                result = response.json()

                st.subheader("Answer")
                st.write(result.get("answer", "No answer found"))

                st.subheader("Sources (Page Numbers)")
                st.write(result.get("sources", []))

            else:
                st.error("Backend not ready yet. Please try again.")