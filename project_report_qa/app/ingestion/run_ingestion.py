import os
from app.ingestion.pdf_loader import load_pdf
from app.ingestion.chunker import chunk_documents
from app.vectorstore.faiss_store import build_faiss_index

PDF_DIR = "data/raw_pdfs"

all_chunks = []

for pdf_file in os.listdir(PDF_DIR):
    if pdf_file.endswith(".pdf"):
        pdf_path = os.path.join(PDF_DIR, pdf_file)
        print(f"Loading {pdf_file}")

        docs = load_pdf(pdf_path)
        chunks = chunk_documents(docs)
        all_chunks.extend(chunks)

print(f"Total chunks created: {len(all_chunks)}")

build_faiss_index(all_chunks)
print("FAISS index created successfully!")
