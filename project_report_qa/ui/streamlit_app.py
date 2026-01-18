import sys
import os
import tempfile
import streamlit as st

# --------------------------------------------------
# Path setup
# --------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

# --------------------------------------------------
# Imports
# --------------------------------------------------
from app.ingestion.pdf_loader import load_pdf
from app.ingestion.chunker import chunk_documents
from app.vectorstore.faiss_store import build_faiss_index
from app.rag.qa_chain import answer_question

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="Project Report QA",
    layout="wide",
)

st.title("📄 Project Report Question Answering")

# --------------------------------------------------
# Session state initialization
# --------------------------------------------------
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "chat" not in st.session_state:
    st.session_state.chat = []

if "docs_processed" not in st.session_state:
    st.session_state.docs_processed = False

# --------------------------------------------------
# File upload section
# --------------------------------------------------
st.subheader("Upload Project Reports")

files = st.file_uploader(
    "Upload one or more project report PDFs",
    type="pdf",
    accept_multiple_files=True,
)

process_clicked = st.button("📌 Process Documents")

if process_clicked:
    if not files:
        st.warning("Please upload at least one PDF file.")
    else:
        with st.spinner("Processing and indexing documents..."):
            try:
                all_chunks = []

                for f in files:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(f.read())
                        tmp_path = tmp.name

                    docs = load_pdf(tmp_path)
                    chunks = chunk_documents(docs)
                    all_chunks.extend(chunks)

                st.session_state.vectorstore = build_faiss_index(all_chunks)
                st.session_state.docs_processed = True

                # Reset chat on new documents
                st.session_state.chat = []

                st.success("✅ Documents indexed successfully. You can now ask questions.")

            except Exception as e:
                st.session_state.vectorstore = None
                st.session_state.docs_processed = False
                st.error(f"❌ Failed to process documents: {e}")

# --------------------------------------------------
# Divider
# --------------------------------------------------
st.divider()

# --------------------------------------------------
# Chat section
# --------------------------------------------------
st.subheader("Ask Questions")

if not st.session_state.docs_processed:
    st.info("Upload and process documents before asking questions.")
else:
    question = st.chat_input("Ask a question about the uploaded documents")

    if question:
        with st.spinner("Generating answer..."):
            try:
                answer = answer_question(
                    question,
                    st.session_state.vectorstore
                )
                st.session_state.chat.append((question, answer))
            except Exception as e:
                st.error(f"❌ Error while answering: {e}")

# --------------------------------------------------
# Chat history display
# --------------------------------------------------
for q, a in st.session_state.chat:
    with st.chat_message("user"):
        st.write(q)

    with st.chat_message("assistant"):
        st.write(a)
