"""
Command line runner for the Music Recommender Simulation.
"""

from src.recommender import load_songs, recommend_songs


def run_profile(songs, profile_name, user_prefs):
    print(f"\n{'='*50}")
    print(f"Profile: {profile_name}")
    print(f"Prefs: {user_prefs}")
    print(f"{'='*50}")
    recommendations = recommend_songs(user_prefs, songs, k=5)
    for rec in recommendations:
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"  Because: {explanation}")


def main() -> None:
    songs = load_songs("data/songs.csv")

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