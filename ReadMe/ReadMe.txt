ReqRAG: Requirements RAG Assistance1. Prerequisites & Setup (Windows friendly)Install Base ToolsPython 3.11+: Download Windows InstallerVS Code: Recommended editor.Ollama (Optional local LLM): Download for WindowsStep 1: Install & Setup OllamaDownload Ollama from ollama.ai (works on Windows, macOS, Linux).Install a model (e.g., LLaMA 3.1 or Mistral) by running this in your terminal:ollama pull llama3
# or
ollama pull mistral

(Note: Keep the Ollama app running in the background).2. Create Project EnvironmentOpen PowerShell in Admin mode and run:mkdir reqrag
cd reqrag
python -m venv .venv

# CAUTION: 'Unrestricted' lowers security. For production/safer dev, use 'Set-ExecutionPolicy RemoteSigned -Scope CurrentUser'
Set-ExecutionPolicy Unrestricted -Force
.\.venv\Scripts\Activate.ps1

3. Install Python PackagesYou can install the core packages needed for the RAG pipeline using pip.Core for RAG (Retrieval + Embeddings)pip install chromadb sentence-transformers

chromadb: Local vector database (stores requirement embeddings).sentence-transformers: Embedding model (MiniLM) for similarity search.Document Processing (PDF/DOCX)pip install pypdf python-docx

pypdf: Read/extract text from PDF files.python-docx: Read Word (.docx) documents.(Optional) pip install unstructured: More robust document parsing.Data Handling / Utilitiespip install tqdm numpy pandas openpyxl

tqdm: Progress bars.numpy: Math & arrays.pandas + openpyxl: Excel export handling.Local LLM Client (for AI Refinement)pip install ollama

Optional Packages (API & Fine-Tuning)If you plan to run the API or fine-tune models later:# Web API (FastAPI)
pip install fastapi uvicorn pydantic httpx

# Fine-Tuning (GPU recommended)
pip install torch --index-url [https://download.pytorch.org/whl/cu121](https://download.pytorch.org/whl/cu121)
pip install transformers accelerate peft trl datasets bitsandbytes

4. Project Structurereqrag/
├── data/
│   ├── raw/              # Put your PDFs/DOCX here
│   ├── processed/        # Auto-generated chunks (JSONL/TXT)
│   └── chroma_db/        # Chroma DB files
├── configs/
│   └── app.yaml
├── app/
│   ├── __init__.py
│   ├── preprocess.py     # Cleaning & Chunking script
│   ├── build_index.py    # Vector DB creation script
│   ├── rag.py            # Main RAG logic & Excel generation
│   ├── prompts.py        # Prompt templates
│   └── api.py            # (Optional) FastAPI backend
├── finetune/             # (Optional) Fine-tuning scripts
│   ├── examples.jsonl
│   ├── sft_dataset.jsonl
│   └── finetune_lora.py
├── client/
│   └── csharp_sample.cs
└── README.md

