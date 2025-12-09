ReqRAG: Requirements RAG Assistance
1. Prerequisites & Setup (Windows friendly)
Install Base Tools
Python 3.11+: Download Windows Installer
VS Code: Recommended editor.
Ollama (Optional local LLM): Download for Windows
Step 1: Install & Setup Ollama

Download Ollama from ollama.ai (works on Windows, macOS, Linux).

Install a model (e.g., LLaMA 3.1 or Mistral) by running this in your terminal:

ollama pull llama3
# or
ollama pull mistral

(Note: Keep the Ollama app running in the background).

2. Create Project Environment

Open PowerShell in Admin mode and run:
mkdir reqrag
cd reqrag
python -m venv .venv

# CAUTION: 'Unrestricted' lowers security. For production/safer dev, use 'Set-ExecutionPolicy RemoteSigned -Scope CurrentUser'
Set-ExecutionPolicy Unrestricted -Force
.\.venv\Scripts\Activate.ps1


3. Install Python Packages
You can install the core packages needed for the RAG pipeline using pip.
Core for RAG (Retrieval + Embeddings)
pip install chromadb sentence-transformers


chromadb: Local vector database (stores requirement embeddings).
sentence-transformers: Embedding model (MiniLM) for similarity search.
Document Processing (PDF/DOCX)
pip install pypdf python-docx


pypdf: Read/extract text from PDF files.
python-docx: Read Word (.docx) documents.
(Optional) pip install unstructured: More robust document parsing.
Data Handling / Utilities
pip install tqdm numpy pandas openpyxl


tqdm: Progress bars.
numpy: Math & arrays.
pandas + openpyxl: Excel export handling.
Local LLM Client (for AI Refinement)
pip install ollama


Optional Packages (API & Fine-Tuning)
If you plan to run the API or fine-tune models later:
# Web API (FastAPI)
pip install fastapi uvicorn pydantic httpx


# Fine-Tuning (GPU recommended)
pip install torch --index-url https://download.pytorch.org/whl/cu121
pip install transformers accelerate peft trl datasets bitsandbytes


4. Project Structure
reqrag/
├── data/
│   ├── raw/              # Put your PDFs/DOCX here
│   ├── processed/        # Auto-generated chunks (JSONL/TXT)
│   └── chroma_db/        # Chroma DB files
├── app/
│   ├── preprocess.py     # Cleaning & Chunking script
│   ├── build_index.py    # Vector DB creation script
│   ├── rag.py            # Main RAG logic & Excel generation
└── README.md


