import os
from dotenv import load_dotenv

load_dotenv()

KNOWLEDGE_BASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'knowledge_base.txt')

def load_knowledge_base():
    """Load and chunk the knowledge base into sections."""
    with open(KNOWLEDGE_BASE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    chunks = [chunk.strip() for chunk in content.split('\n\n') if chunk.strip()]
    return chunks

def retrieve_context(query: str, top_k: int = 3) -> str:
    """Retrieve the most relevant chunks from the knowledge base."""
    chunks = load_knowledge_base()
    query_words = set(query.lower().split())
    
    scored = []
    for chunk in chunks:
        chunk_words = set(chunk.lower().split())
        score = len(query_words & chunk_words)
        scored.append((score, chunk))
    
    scored.sort(reverse=True, key=lambda x: x[0])
    top_chunks = [chunk for score, chunk in scored[:top_k] if score > 0]
    
    if not top_chunks:
        return "No specific context found for this query."
    
    return "\n\n".join(top_chunks)

if __name__ == "__main__":
    test_query = "happy pop music"
    context = retrieve_context(test_query)
    print(f"Query: {test_query}")
    print(f"\nRetrieved Context:\n{context}")