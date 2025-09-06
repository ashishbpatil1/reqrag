import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path
import pandas as pd

DB_DIR = Path("data/chroma_db")
OUTPUT_FILE = Path("data/user_stories.xlsx")

def estimate_effort(text: str) -> int:
    """
    Very simple heuristic:
    - Short/simple requirements = 4h
    - Medium complexity = 8h
    - Longer/complex = 16h
    """
    length = len(text.split())
    if length < 12:
        return 4
    elif length < 30:
        return 8
    elif length < 60:
        return 16
    else:
        return 24

def refine_to_user_story(requirement: str):
    """
    Converts raw requirement text to Jira-ready story format.
    """
    summary = " ".join(requirement.split()[:5]) + "..."
    user_story = f"As a user, I want to {requirement.lower()} so that I can achieve my goal effectively."
    description = f"Requirement extracted from document:\n\n{requirement}"
    acceptance_criteria = [
        "The functionality works as expected with valid inputs.",
        "Errors are handled gracefully with invalid inputs.",
        "The feature is testable and meets security/performance needs."
    ]
    effort = estimate_effort(requirement)

    return {
        "Summary": summary,
        "User Story": user_story,
        "Description": description,
        "Acceptance Criteria": "; ".join(acceptance_criteria),
        "Estimated Effort (Hours)": effort
    }

def query_and_refine(query: str, top_k: int = 5):
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
        story = refine_to_user_story(doc)
        stories.append(story)

    df = pd.DataFrame(stories)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(OUTPUT_FILE, index=False, sheet_name="UserStories")

    print(f"✅ User Stories saved to {OUTPUT_FILE}")
    return df

if __name__ == "__main__":
    q = "List all requirements related to login functionality"
    df = query_and_refine(q, top_k=10)
    print(df)
