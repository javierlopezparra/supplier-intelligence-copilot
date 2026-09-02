# Supplier Intelligence Copilot

AI-powered RAG assistant for supplier document intelligence
and procurement workflows.

## Problem

Supplier and procurement teams manage large volumes of
documents containing information such as:

- Lead times
- Payment terms
- Certifications
- Capacity
- Products
- Coverage
- Commercial conditions

Finding this information manually can be slow and repetitive.

## Solution

Supplier Intelligence Copilot transforms supplier documents
into a searchable semantic knowledge base.

The system currently:

1. Reads supplier PDF documents
2. Extracts document text
3. Splits text into contextual chunks
4. Generates multilingual embeddings
5. Performs semantic search
6. Retrieves the most relevant information for a question

## Example

Question:

"¿Cuánto tarda el proveedor en entregar?"

Retrieved context:

"Lead Time: 15 calendar days"

Similarity score: 0.5095

## Architecture

PDF
↓
Document Loader
↓
Text Chunking
↓
Embeddings
↓
Semantic Search
↓
Vector Store
↓
RAG
↓
LLM

## Tech Stack

- Python
- PyPDF
- Sentence Transformers
- NumPy
- Hugging Face
- ChromaDB (next stage)
- Docker (planned)

## Project Status

- [x] PDF ingestion
- [x] Text extraction
- [x] Chunking
- [x] Multilingual embeddings
- [x] Semantic search
- [ ] Persistent vector database
- [ ] RAG response generation
- [ ] Source citations
- [ ] API
- [ ] Docker
- [ ] Azure deployment
