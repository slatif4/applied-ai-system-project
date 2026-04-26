import os
import sys
import warnings
warnings.filterwarnings("ignore")

from dotenv import load_dotenv
load_dotenv()

# Add src to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from recommender import load_songs, recommend_songs
from rag import retrieve_context
from agent import search_new_music
from explainer import generate_explanation

# Path to songs CSV
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'songs.csv')

def run_vibefinder(mood: str, genre: str, energy: float = 0.7) -> dict:
    """
    Main pipeline: takes user input and returns full recommendations.
    Combines recommender + RAG + agent + explainer.
    """
    print(f"\n🎵 VibeFinder 2.0 — searching for {mood} {genre} music...\n")

    # Step 1: Load songs and get recommendations
    songs = load_songs(CSV_PATH)
    user_prefs = {
        "genre": genre,
        "mood": mood,
        "energy": energy
    }
    recommendations = recommend_songs(user_prefs, songs, k=5)
    song_list = [{"title": s["title"], "artist": s["artist"]} for s, _, _ in recommendations]

    print(f"[Recommender] Found {len(song_list)} songs")

    # Step 2: RAG - retrieve context from knowledge base
    rag_query = f"{mood} {genre} music"
    rag_context = retrieve_context(rag_query)
    print(f"[RAG] Retrieved context for: {rag_query}")

    # Step 3: Agent - search Wikipedia for live context
    wiki_context = search_new_music(mood, genre)
    print(f"[Agent] Retrieved Wikipedia context")

    # Step 4: Generate AI explanation
    explanation = generate_explanation(mood, genre, song_list, rag_context, wiki_context)
    print(f"[Explainer] Generated explanation")

    return {
        "mood": mood,
        "genre": genre,
        "recommendations": song_list,
        "rag_context": rag_context,
        "wiki_context": wiki_context,
        "explanation": explanation
    }


if __name__ == "__main__":
    result = run_vibefinder("happy", "pop")

    print("\n=== RECOMMENDATIONS ===")
    for i, song in enumerate(result["recommendations"], 1):
        print(f"{i}. {song['title']} by {song['artist']}")

    print("\n=== AI EXPLANATION ===")
    print(result["explanation"])

    print("\n=== WIKIPEDIA CONTEXT ===")
    print(result["wiki_context"][:300])