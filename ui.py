import streamlit as st
import requests

st.title("PDF Chatbot")

pdf = st.file_uploader("Upload PDF")

if pdf:

    files = {"file": pdf}

    res = requests.post("http://localhost:8000/upload", files=files)

    st.write(res.json())

question = st.text_input("Ask question")

if st.button("Ask"):

    res = requests.post(
        "http://localhost:8000/ask",
        json={"question": question}
    )

    st.write(res.json()["answer"])