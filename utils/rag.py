import os
import sys
import fitz

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models.embeddings import chunk_text, build_vector_store, retrieve_relevant_chunks

def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        full_text = ""
        for page in doc:
            full_text += page.get_text() + "\n"
        doc.close()
        return full_text.strip()
    except Exception as e:
        raise RuntimeError(f"Could not read PDF file: {str(e)}")

def extract_text_from_txt(file_bytes: bytes) -> str:
    try:
        try:
            return file_bytes.decode("utf-8").strip()
        except UnicodeDecodeError:
            return file_bytes.decode("latin-1").strip()
    except Exception as e:
        raise RuntimeError(f"Could not read text file: {str(e)}")

def process_uploaded_file(uploaded_file) -> tuple:
    try:
        file_bytes = uploaded_file.read()
        file_name  = uploaded_file.name.lower()

        if file_name.endswith(".pdf"):
            raw_text = extract_text_from_pdf(file_bytes)
        elif file_name.endswith(".txt"):
            raw_text = extract_text_from_txt(file_bytes)
        else:
            raise ValueError("Unsupported file type. Please upload a PDF or TXT file.")

        if not raw_text:
            raise ValueError("The uploaded file appears to be empty or unreadable.")

        chunks = chunk_text(raw_text)
        if not chunks:
            raise ValueError("Could not extract any chunks from the file.")

        index, chunks = build_vector_store(chunks)
        return index, chunks, raw_text

    except Exception as e:
        raise RuntimeError(f"File processing failed: {str(e)}")

def get_rag_context(query: str, index, chunks: list[str]) -> tuple[str, bool]:
    try:
        relevant_chunks, best_score = retrieve_relevant_chunks(query, index, chunks)
        if not relevant_chunks:
            return "", False

        context_text = "\n\n---\n\n".join(relevant_chunks)
        return context_text, True
    except Exception as e:
        return "", False
