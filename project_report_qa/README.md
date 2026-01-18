📄 Project Report Question Answering System (RAG-Based)
Overview

This project is a Document Question Answering application designed to extract and answer questions from multiple semi-structured project reports (PDFs) such as capital project reports, feasibility studies, and industrial assessments.

The system allows users to:

Upload one or more PDF documents

Ask natural language questions

Receive accurate, structured answers

View clear source attribution and evidence from the documents

The solution uses a Retrieval-Augmented Generation (RAG) approach to combine deterministic data extraction with LLM-based contextual understanding, ensuring both accuracy and flexibility.

🎯 Key Features
1. Working Application with Interface

Web-based interface built using Streamlit

Upload multiple PDF documents at once

Chat-style interaction (similar to ChatGPT)

Clear separation between document upload and question-answering phases

Answers include:

Extracted information

Source document reference

Supporting evidence (direct quotes)

2. Multi-Document Support

Handles multiple PDFs simultaneously

Treats each PDF as an independent project

Prevents mixing information across documents

Supports comparative and multi-project queries

3. Flexible Question Answering

Users can ask:

Structured questions
“What is the project budget?”
“Where is the project located?”

Compound questions
“What are the budgets and locations of these projects?”

Descriptive questions
“What is the scope of the project?”
“Explain the project overview.”

🧠 High-Level Architecture
User Uploads PDFs
        ↓
PDF Text Extraction & Chunking
        ↓
Vector Index Creation (FAISS)
        ↓
User Question
        ↓
Intent Detection
        ↓
Hybrid Retrieval (Semantic + Keyword)
        ↓
Re-ranking
        ↓
Document-wise Grouping
        ↓
 ┌──────────────────────────────┐
 │ Extractive Path (Facts)       │
 │ - Budget, Location, Owner     │
 │ - Deterministic Extraction    │
 └──────────────────────────────┘
                +
 ┌──────────────────────────────┐
 │ Descriptive Path (LLM)        │
 │ - Scope, Summary, Explanation │
 │ - Contextual Answering        │
 └──────────────────────────────┘
        ↓
Final Answer with Sources & Evidence

🛠️ Technology Stack
Frontend

Streamlit

Simple, fast web UI

Chat-style interface

Session-based state management

Backend

Python (core implementation)

LangChain (prompt handling, LLM wrappers)

FAISS (vector storage and similarity search)

Language Model

FLAN-T5 (local LLM) via HuggingFace

Used only for:

Descriptive questions (scope, summary, explanation)

Final answer presentation

Not used for fact extraction (prevents hallucination)

Embeddings

Sentence/transformer-based embeddings

Stored locally using FAISS

No dependency on external APIs

🔍 RAG Implementation Approach
Why RAG?

Traditional LLMs:

Can hallucinate

Lack document traceability

Are unreliable for factual extraction

RAG solves this by:

Retrieving relevant document context first

Restricting LLM responses to verified content

Hybrid Retrieval Strategy

The system uses a hybrid retrieval approach:

Semantic Search

Finds conceptually relevant content

Keyword Boosting

Improves precision for domain-specific terms

Re-ranking

Ensures most relevant chunks are prioritized

This balances recall and precision, especially for semi-structured PDFs.

🧩 Intent-Based Question Handling

Questions are classified into two categories:

1. Extractive (Deterministic)

Handled without LLM inference.

Examples:

Budget

Location

Project name

Owner / company

Timeline

Approach:

Signal-based extraction (numbers, dates, proper nouns)

Robust to changes in field names (e.g., “TIV”, “Total Investment”)

2. Descriptive (LLM-Based)

Handled using LLM with retrieved context.

Examples:

Project scope

Overview / explanation

Background / history

Approach:

Relevant chunks are passed to the LLM

Strict prompts prevent hallucination

Answers are grounded in document text

🧪 Evidence and Source Attribution

Every answer includes:

Document identifier (PDF-1, PDF-2, etc.)

Page number

Exact supporting quotes

This ensures:

Transparency

Auditability

Trustworthiness

🚧 Challenges Faced & Solutions
Challenge 1: Semi-Structured PDFs

Problem:
Field names and layouts vary across documents.

Solution:
Used signal-based extraction (patterns, numeric magnitude, context windows) instead of strict field matching.

Challenge 2: Mixed Question Types

Problem:
Users ask both factual and descriptive questions.

Solution:
Implemented intent detection and routed questions through:

Deterministic extractors (for facts)

LLM fallback (for explanations)

Challenge 3: Hallucination Risk

Problem:
LLMs can invent information.

Solution:

LLM is never used for fact extraction

Strict prompts: “Use only provided context”

Clear fallback when information is missing

Challenge 4: Multi-PDF Confusion

Problem:
Information from different documents could mix.

Solution:

Group chunks by document

Enforce “one PDF = one project”

Answer per document

✅ Why This Approach Is Effective

Combines accuracy (deterministic extraction)

With flexibility (LLM explanations)

Works for real-world industrial documents

Scales to new document formats

Suitable for production and enterprise use

📌 How to Run the Application
pip install -r requirements.txt
streamlit run ui/streamlit_app.py

📂 Project Structure (Simplified)
app/
 ├─ ingestion/        # PDF loading & chunking
 ├─ vectorstore/      # FAISS indexing & retrieval
 ├─ rag/              # QA logic, extractors, prompts
ui/
 └─ streamlit_app.py  # Web interface

👤 Author

Sachin Balhara
AI / ML Engineer