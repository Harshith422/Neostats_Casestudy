import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from config.config import CHUNK_SIZE, CHUNK_OVERLAP, TOP_K_RESULTS, SIMILARITY_THRESHOLD

_embedding_model = None

def get_embedding_model():
    """Load and cache the embedding model."""
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedding_model

def chunk_text(text: str) -> list[str]:
    """Split text into smaller, overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks

def build_vector_store(chunks: list[str]) -> tuple:
    """Convert text chunks to embeddings and build a FAISS index."""
    try:
        model = get_embedding_model()
        embeddings = model.encode(chunks, show_progress_bar=False)
        embeddings = np.array(embeddings, dtype="float32")
        faiss.normalize_L2(embeddings)

        dimension = embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)
        index.add(embeddings)

        return index, chunks
    except Exception as e:
        raise RuntimeError(f"Failed to build vector store: {str(e)}")

def retrieve_relevant_chunks(query: str, index, chunks: list[str]) -> tuple[list[str], float]:
    """Find the most relevant chunks for a given query."""
    try:
        model = get_embedding_model()
        query_vec = model.encode([query], show_progress_bar=False)
        query_vec = np.array(query_vec, dtype="float32")
        faiss.normalize_L2(query_vec)

        scores, indices = index.search(query_vec, TOP_K_RESULTS)
        best_score = float(scores[0][0]) if len(scores[0]) > 0 else 0.0

        relevant = []
        for score, idx in zip(scores[0], indices[0]):
            if score >= SIMILARITY_THRESHOLD and idx < len(chunks):
                relevant.append(chunks[idx])

        return relevant, best_score
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve chunks: {str(e)}")
