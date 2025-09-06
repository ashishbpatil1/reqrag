import os
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

PROCESSED_DIR = Path("data/processed")
DB_DIR = Path("data/chroma_db")
DB_DIR.mkdir(parents=True, exist_ok=True)

def build_index():
    """Read processed text files and insert chunks into Chroma DB (local only)."""
    # Embedding model (small + fast, downloads once)
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    # Chroma persistent client
    client = chromadb.PersistentClient(path=str(DB_DIR))
    collection = client.get_or_create_collection("requirements")

    for file_path in PROCESSED_DIR.glob("*.txt"):
        print(f"📄 Indexing {file_path.name}...")

        with open(file_path, "r", encoding="utf-8") as f:
            chunks = [line.strip() for line in f if line.strip()]

        if not chunks:
            print(f"⚠️ Skipping empty file: {file_path.name}")
            continue

        # Create embeddings
        embeddings = [embedder.encode(chunk).tolist() for chunk in chunks]

        # Add chunks to Chroma
        collection.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=[{"source": file_path.name} for _ in chunks],
            ids=[f"{file_path.stem}_{i}" for i in range(len(chunks))]
        )

        print(f"✅ Indexed {len(chunks)} chunks from {file_path.name}")

    print("🎉 Index build complete! Vector DB saved at:", DB_DIR)

if __name__ == "__main__":
    build_index()
