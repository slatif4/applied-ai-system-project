import os
import wikipediaapi
from dotenv import load_dotenv

load_dotenv()

wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='VibeFinder/2.0 (AI110 Final Project)'
)

def search_new_music(mood: str, genre: str) -> str:
    """Use Wikipedia to retrieve music context for the given genre and mood."""
    print(f"[Agent] Searching Wikipedia for {mood} {genre} music...")

    try:
        # Search for the genre page
        search_term = f"{genre} music"
        page = wiki.page(search_term)

        if page.exists():
            # Get first 1000 characters of the summary
            summary = page.summary[:1000]
            result = f"**About {genre.title()} Music:**\n{summary}\n\n"
            result += f"*This context was retrieved live from Wikipedia to help match your {mood} {genre} vibe.*"
            return result
        else:
            return f"No Wikipedia article found for {genre} music."

    except Exception as e:
        print(f"[Agent] Search failed: {e}")
        return f"Search unavailable: {str(e)}"


if __name__ == "__main__":
    result = search_new_music("happy", "pop")
    print("\n=== Agent Search Result ===")
    print(result)