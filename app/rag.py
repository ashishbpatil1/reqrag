import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path
import pandas as pd
import ollama  # local LLM

DB_DIR = Path("data/chroma_db")
OUTPUT_FILE = Path("data/user_stories.xlsx")

def generate_story_with_llm(requirement: str) -> dict:
    """
    Calls Ollama LLM to refine requirement into Jira-ready user story.
    """
    prompt = f"""
    You are a Senior Requirements Analyst.
    Convert the following requirement into a Jira user story with:
    - Summary
    - User Story (As a <user>, I want <action>, so that <benefit>)
    - Description
    - Acceptance Criteria (3 points, testable)
    - Estimated Effort in hours (small=4h, medium=8h, large=16h, XL=24h)

    Requirement: "{requirement}"
    """

    response = ollama.chat(
        model="llama3",  # or "mistral", depending on what you pulled
        messages=[
            {"role": "system", "content": "You are a Senior Requirements Analyst."},
            {"role": "user", "content": prompt}
        ]
    )

    content = response["message"]["content"]

    # crude split (LLM outputs formatted text)
    # we’ll just return as a single text block for now
    return {
        "Requirement": requirement,
        "LLM Generated Story": content
    }

def query_and_refine_with_llm(query: str, top_k: int = 5):
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path=str(DB_DIR))
    collection = client.get_collection("requirements")

    query_emb = embedder.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_emb],
        n_results=top_k
    )

    stories = []
    for doc in results["documents"][0]:
        story = generate_story_with_llm(doc)
        stories.append(story)

    df = pd.DataFrame(stories)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(OUTPUT_FILE, index=False, sheet_name="UserStories")

    print(f"✅ User Stories saved to {OUTPUT_FILE}")
    return df

if __name__ == "__main__":
    q = "List all requirements related to login functionality"
    df = query_and_refine_with_llm(q, top_k=5)
    print(df)
