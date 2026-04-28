"""
Command line runner for the Music Recommender Simulation.
"""

from pathlib import Path
from src.recommender import load_songs, recommend_songs
from tabulate import tabulate


def run_profile(songs, profile_name, user_prefs):
    print(f"\n{'='*60}")
    print(f"Profile: {profile_name}")
    print(f"Prefs: {user_prefs}")
    print(f"{'='*60}")
    
    recommendations = recommend_songs(user_prefs, songs, k=5)
    
    table_data = []
    for rank, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        table_data.append([rank, song['title'], song['artist'], score, explanation])
    
    headers = ["Rank", "Title", "Artist", "Score", "Reasons"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def main() -> None:
    data_file = Path(__file__).resolve().parents[1] / "data" / "songs.csv"
    songs = load_songs(str(data_file))

    # Profile 1: High-Energy Pop
    run_profile(songs, "High-Energy Pop", {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.9
    })

    # Profile 2: Chill Lofi
    run_profile(songs, "Chill Lofi", {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.35
    })

    # Profile 3: Deep Intense Rock
    run_profile(songs, "Deep Intense Rock", {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.95
    })


if __name__ == "__main__":
    main()