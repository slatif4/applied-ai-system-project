import os
import warnings
warnings.filterwarnings("ignore")
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MOOD_DESCRIPTIONS = {
    "happy": "upbeat, energizing, and full of positive energy",
    "sad": "emotional, introspective, and deeply moving",
    "energetic": "high-tempo, powerful, and motivating",
    "chill": "relaxed, smooth, and easygoing",
    "romantic": "warm, intimate, and heartfelt",
    "focused": "steady, calming, and non-distracting"
}

GENRE_DESCRIPTIONS = {
    "pop": "catchy melodies, polished production, and broad appeal",
    "rock": "electric guitars, strong rhythms, and powerful vocals",
    "hip-hop": "rhythmic beats, lyrical storytelling, and cultural depth",
    "jazz": "improvisation, complex harmonies, and sophisticated atmosphere",
    "electronic": "synthesizers, digital production, and dynamic energy",
    "r&b": "soulful vocals, rhythm, and emotional expression",
    "classical": "orchestral arrangements and timeless emotional depth"
}

def generate_explanation(mood: str, genre: str, songs: list, rag_context: str, wiki_context: str) -> str:
    """Use Gemini to explain why the recommended songs match the user's vibe.
    Falls back to rule-based explanation if API is unavailable."""
    print(f"[Explainer] Generating explanation for {mood} {genre} recommendations...")

    song_list = "\n".join([f"- {s['title']} by {s['artist']}" for s in songs[:3]])

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = f"""You are a music expert. A user wants {mood} {genre} music.

Knowledge base context:
{rag_context}

Wikipedia context:
{wiki_context}

Recommended songs:
{song_list}

In 3-4 sentences, explain why these songs are a great match for someone looking for {mood} {genre} music.
Be friendly and specific."""

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(f"[Explainer] Gemini unavailable, using rule-based fallback: {e}")
        mood_desc = MOOD_DESCRIPTIONS.get(mood.lower(), "emotionally resonant and engaging")
        genre_desc = GENRE_DESCRIPTIONS.get(genre.lower(), "musically rich and diverse")
        song_titles = [f"{s['title']} by {s['artist']}" for s in songs[:3]]
        song_list_str = ", ".join(song_titles[:-1]) + f", and {song_titles[-1]}" if len(song_titles) > 1 else song_titles[0]

        return (
            f"Based on your preference for **{mood} {genre}** music, we found songs that are {mood_desc} "
            f"while featuring {genre_desc}. "
            f"Tracks like {song_list_str} were selected because they closely match your mood and genre profile. "
            f"Our knowledge base confirmed that {genre} music is known for {genre_desc}, "
            f"making these tracks an ideal fit for your current vibe."
        )


if __name__ == "__main__":
    test_songs = [
        {"title": "Blinding Lights", "artist": "The Weeknd"},
        {"title": "Levitating", "artist": "Dua Lipa"},
        {"title": "Happy", "artist": "Pharrell Williams"}
    ]
    rag_context = "Pop music features catchy melodies and broad appeal. Happy music is upbeat and energizing."
    wiki_context = "Pop music originated in the 1950s and is characterized by repeated choruses and hooks."

    result = generate_explanation("happy", "pop", test_songs, rag_context, wiki_context)
    print("\n=== Explanation ===")
    print(result)