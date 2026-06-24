# LexRAG — Legal Contract Intelligence Engine

A Retrieval-Augmented Generation (RAG) system that lets you ask natural language questions about legal contracts and get grounded, citation-backed answers. Built from scratch to understand every layer of a modern RAG pipeline — not just wiring together a framework.

## What it does

Upload a legal document (NDA, employment contract, lease agreement, etc.) and ask questions like:
- "What is the termination notice period?"
- "What happens if either party breaches confidentiality?"
- "Who has the right to terminate this agreement?"

The system retrieves the most relevant clauses using **hybrid search** (combining semantic similarity and keyword matching) and generates an answer with the exact page/clause it came from — so answers are always traceable, never hallucinated black boxes.

## Why hybrid search

Pure semantic (dense vector) search is great at understanding meaning but can miss exact terms — like specific defined terms, section numbers, or party names that matter a lot in legal text. Pure keyword search (BM25) catches exact matches but misses paraphrased questions. This project combines both and merges results using **Reciprocal Rank Fusion (RRF)**, giving more reliable retrieval than either method alone.

## Architecture

```
PDF Upload
    │
    ▼
pdf_loader.py     → extracts text page by page (PyMuPDF)
    │
    ▼
chunker.py        → splits into overlapping chunks (LangChain)
    │
    ▼
embedder.py       → converts chunks to dense vectors (sentence-transformers)
    │
    ▼
vector_store.py   → stores vectors in ChromaDB
    │
    ▼
retriever.py      → hybrid search: dense (ChromaDB) + sparse (BM25) → RRF merge
    │
    ▼
llm_chain.py      → top chunks + question → Groq (Llama 3.3 70B) → grounded answer
    │
    ▼
app.py            → Streamlit interface for upload + Q&A
```

## Tech Stack

| Component | Tool |
|---|---|
| PDF parsing | PyMuPDF |
| Chunking | LangChain RecursiveCharacterTextSplitter |
| Dense embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| Vector store | ChromaDB |
| Sparse retrieval | BM25 (`rank-bm25`) |
| Reranking | Reciprocal Rank Fusion (RRF) |
| LLM | Groq API — Llama 3.3 70B |
| UI | Streamlit |
| Deployment | HuggingFace Spaces |

## Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/lexrag.git
cd lexrag

# Create virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add your Groq API key
cp .env.example .env
# then edit .env and paste your key
```

## Usage

```bash
# Ingest a document
python ingest.py data/your_contract.pdf

# Query from command line
python ingest.py --query "What is the termination notice period?"

# Run the Streamlit app
streamlit run app.py
```

## Project Structure

```
lexrag/
├── src/
│   ├── pdf_loader.py      # PDF → page-level text
│   ├── chunker.py         # Text → overlapping chunks
│   ├── embedder.py        # Chunks → dense vectors
│   ├── vector_store.py    # ChromaDB storage + dense search
│   ├── retriever.py       # Hybrid search (dense + BM25 + RRF)
│   └── llm_chain.py       # Answer generation with Groq
├── data/                  # Sample contracts (not tracked in git)
├── ingest.py               # CLI entry point for ingestion + querying
├── app.py                  # Streamlit UI
├── requirements.txt
├── .env.example
└── README.md
```

## Status

🚧 Work in progress — building in public, lesson by lesson.

- [x] PDF loading
- [x] Chunking
- [ ] Dense embeddings + ChromaDB
- [ ] BM25 sparse retrieval
- [ ] Hybrid search with RRF
- [ ] LLM answer generation
- [ ] Streamlit UI
- [ ] Deployment

## Learnings

This project was built to understand RAG internals deeply — not just call a LangChain function and move on. Each module was written and tested independently before being wired together.

## License

MIT
