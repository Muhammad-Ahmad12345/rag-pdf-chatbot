import fitz
import re


def extract_text_from_pdf(file_path):

    doc = fitz.open(file_path)

    pages = []

    for page_num in range(len(doc)):

        page = doc.load_page(page_num)

        text = page.get_text("text")

        if text.strip():

            pages.append({
                "page": page_num + 1,
                "text": text
            })

    return pages


def chunk_text(text, chunk_size=700, overlap=100):
    paragraphs = re.split(r'\n\s*\n', text)

    chunks = []
    current_chunk = ""

    for para in paragraphs:

        if len(current_chunk) + len(para) < chunk_size:

            current_chunk += " " + para

        else:

            chunks.append(current_chunk.strip())

            current_chunk = para

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks