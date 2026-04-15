from typing import List, Dict, Tuple
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """Represents a song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """OOP implementation of the recommendation logic."""
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = []
        for song in self.songs:
            prefs = {
                "genre": user.favorite_genre,
                "mood": user.favorite_mood,
                "energy": user.target_energy
            }
            song_dict = {
                "genre": song.genre,
                "mood": song.mood,
                "energy": song.energy,
                "title": song.title
            }
            score, _ = score_song(prefs, song_dict)
            scored.append((song, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [s[0] for s in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append(f"genre match ({song.genre})")
        if song.mood == user.favorite_mood:
            reasons.append(f"mood match ({song.mood})")
        energy_gap = abs(song.energy - user.target_energy)
        if energy_gap < 0.2:
            reasons.append(f"energy is close to your target ({song.energy:.2f})")
        return ", ".join(reasons) if reasons else "general match"


def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file and returns a list of dictionaries."""
    songs = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['energy'] = float(row['energy'])
            row['tempo_bpm'] = float(row['tempo_bpm'])
            row['valence'] = float(row['valence'])
            row['danceability'] = float(row['danceability'])
            row['acousticness'] = float(row['acousticness'])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Algorithm Recipe:
      +2.0 for genre match
      +1.0 for mood match
      +1.0 similarity points based on energy closeness
    Returns (score, reasons)
    """
    score = 0.0
    reasons = []

    # Genre match
    if song.get('genre') == user_prefs.get('genre'):
        score += 2.0
        reasons.append(f"genre match (+2.0)")

    # Mood match
    if song.get('mood') == user_prefs.get('mood'):
        score += 1.0
        reasons.append(f"mood match (+1.0)")

    # Energy similarity (closer = higher score)
    energy_gap = abs(float(song.get('energy', 0)) - float(user_prefs.get('energy', 0.5)))
    energy_score = round(1.0 - energy_gap, 2)
    score += energy_score
    reasons.append(f"energy similarity ({energy_score:.2f})")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Scores and ranks all songs, returns top k recommendations.
    Returns list of (song_dict, score, explanation)
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]