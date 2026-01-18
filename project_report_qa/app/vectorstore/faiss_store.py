import os
from langchain.vectorstores import FAISS
from app.ingestion.embedder import get_embedding_model
import app.config as config


def build_faiss_index(chunks):
    embeddings = get_embedding_model()
    vectorstore = FAISS.from_documents(chunks, embeddings)

    os.makedirs(config.settings.FAISS_INDEX_PATH, exist_ok=True)
    vectorstore.save_local(config.settings.FAISS_INDEX_PATH)

    return vectorstore
