1) Prerequisites & Setup (Windows friendly)

Install
Python 3.11+ -> https://www.python.org/ftp/python/3.13.7/python-3.13.7-amd64.exe
VS Code 
(Optional local LLM) Ollama llama3.1:8b -> https://ollama.com/download/windows


2) Create project:
# In PowerShell admin mode:

mkdir reqrag && cd reqrag
python -m venv .venv
Set-ExecutionPolicy Unrestricted -Force
.\.venv\Scripts\Activate.ps1

3) Install Python packages
CPU‑only is fine for RAG. Fine‑tuning needs a GPU; keep those packages optional.
pip install chromadb sentence-transformers pypdf python-docx unstructured
pip install fastapi uvicorn pydantic
pip install httpx tqdm numpy pandas
# Optional, for local LLM via Ollama client
pip install ollama
# Optional, for Transformers pipeline (CPU ok for inference; slow)
pip install transformers accelerate
# Optional, for fine-tuning (GPU recommended)
pip install torch --index-url https://download.pytorch.org/whl/cu121 # or 'pip install torch' for CPU
pip install peft trl datasets bitsandbytes # bitsandbytes requires CUDA; skip if CPU-only

Installed Packages So Far
🔹 Core for RAG (retrieval + embeddings)
pip install chromadb
pip install sentence-transformers


chromadb → local vector database (stores requirement embeddings).

sentence-transformers → embedding model (MiniLM) for similarity search.

🔹 Document Processing (PDF/DOCX)
pip install pypdf
pip install python-docx
pip install unstructured


pypdf → read/extract text from PDF files.

python-docx → read Word (.docx) documents.

unstructured → more robust document parsing (optional but handy).

🔹 Web API (for microservices / UI integration)
pip install fastapi uvicorn pydantic
pip install httpx


fastapi → REST API backend (Python microservice).

uvicorn → ASGI server to run FastAPI.

pydantic → input/output data validation.

httpx → HTTP client (if Python service calls other APIs).

🔹 Data Handling / Utilities
pip install tqdm numpy pandas


tqdm → progress bars in loops.

numpy → math & arrays (used under the hood by embeddings).

pandas → for tabular data + Excel export.

🔹 Excel Export
pip install openpyxl


openpyxl → required by pandas to write .xlsx.


Step 1: Install Ollama

Download Ollama from https://ollama.ai

(works on Windows, macOS, Linux).

Install a model, e.g. LLaMA 3.1 or Mistral:

ollama pull llama3
# or
ollama pull mistral

🔹 Step 2: Install Python client for Ollama 🔹 Local LLM (optional, if you want AI refinement)
pip install ollama


ollama → Python client for local models (Llama, Mistral, etc.).

Works with the Ollama desktop app running in background.


4) Project structure

reqrag/
data/
raw/ # put your PDFs/DOCX here
processed/ # auto-generated chunks JSONL
index/ # Chroma DB files
configs/
app.yaml
app/
__init__.py
preprocess.py
build_index.py
rag.py
prompts.py
api.py
finetune/
examples.jsonl
sft_dataset.jsonl
finetune_lora.py
client/
csharp_sample.cs
README.md

