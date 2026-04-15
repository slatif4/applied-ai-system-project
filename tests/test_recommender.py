from src.recommender import Song, UserProfile, Recommender, score_song, load_songs


def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)
    assert len(results) == 2
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]
    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_score_song_genre_match_adds_two_points():
    user_prefs = {"genre": "pop", "mood": "sad", "energy": 0.5}
    song = {"genre": "pop", "mood": "happy", "energy": 0.5}
    score, reasons = score_song(user_prefs, song)
    assert score >= 2.0
    assert any("genre match" in r for r in reasons)


def test_score_song_mood_match_adds_one_point():
    user_prefs = {"genre": "rock", "mood": "happy", "energy": 0.5}
    song = {"genre": "pop", "mood": "happy", "energy": 0.5}
    score, reasons = score_song(user_prefs, song)
    assert score >= 1.0
    assert any("mood match" in r for r in reasons)


def test_score_song_perfect_match():
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    song = {"genre": "pop", "mood": "happy", "energy": 0.8}
    score, reasons = score_song(user_prefs, song)
    assert score == 4.0


def test_recommend_returns_correct_count():
    user = UserProfile(
        favorite_genre="lofi",
        favorite_mood="chill",
        target_energy=0.4,
        likes_acoustic=True,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=1)
    assert len(results) == 1


def test_load_songs_returns_list():
    songs = load_songs("data/songs.csv")
    assert isinstance(songs, list)
    assert len(songs) == 20