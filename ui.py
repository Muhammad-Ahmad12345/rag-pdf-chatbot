import streamlit as st

st.title("RAG PDF Chatbot")

st.write("Upload a PDF and ask questions")

pdf = st.file_uploader("Upload PDF")

question = st.text_input("Ask a question")

if st.button("Ask"):
    st.write("Answer will appear here")