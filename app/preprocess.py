import os, json, re
from pathlib import Path
from typing import List, Dict
from pypdf import PdfReader
from docx import Document


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# --- simple cleaners ---
def clean_text(t: str) -> str:
    t = re.sub(r"\u00a0", " ", t) # non-breaking spaces
    t = re.sub(r"[\t\r]", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200):
    """Yield chunks of text with overlap."""
    start = 0
    while start < len(text):
        yield text[start:start + chunk_size]
        start += chunk_size - overlap

def process_pdf(file_path: Path):
    """Extract text from PDF page by page, yield chunks."""
    reader = PdfReader(str(file_path))
    for page in reader.pages:
        text = page.extract_text() or ""
        text = clean_text(text)
        if text:
            for chunk in chunk_text(text):
                yield chunk

def process_docx(file_path: Path):
    """Extract text from DOCX paragraph by paragraph, yield chunks."""
    doc = docx.Document(str(file_path))
    buffer = ""
    for para in doc.paragraphs:
        buffer += " " + para.text
        if len(buffer) > 800:  # flush every ~800 chars to keep memory small
            buffer = clean_text(buffer)
            for chunk in chunk_text(buffer):
                yield chunk
            buffer = ""
    if buffer.strip():
        buffer = clean_text(buffer)
        for chunk in chunk_text(buffer):
            yield chunk

def preprocess_all():
    """Process all files in RAW_DIR and save chunks into PROCESSED_DIR."""
    for file_path in RAW_DIR.iterdir():
        if not file_path.is_file():
            continue

        print(f"Processing {file_path.name}...")
        chunks = []

        if file_path.suffix.lower() == ".pdf":
            chunks = list(process_pdf(file_path))
        elif file_path.suffix.lower() in [".docx", ".doc"]:
            chunks = list(process_docx(file_path))
        else:
            print(f"Skipping unsupported file: {file_path.name}")
            continue

        # Write chunks to processed folder
        out_file = PROCESSED_DIR / f"{file_path.stem}.txt"
        with open(out_file, "w", encoding="utf-8") as f:
            for chunk in chunks:
                f.write(chunk + "\n")

        print(f"✅ Saved {len(chunks)} chunks to {out_file}")

if __name__ == "__main__":
    preprocess_all()