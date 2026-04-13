from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with numeric fields cast to int or float."""
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences using weighted proximity; return (score, reasons)."""
    TEMPO_MIN = 60.0
    TEMPO_MAX = 200.0

    WEIGHTS = {
        "mood":         1.5,
        "energy":       1.5,
        "acousticness": 1.0,
        "valence":      1.0,
        "danceability": 1.0,
        "tempo":        1.0,
    }

    score = 0.0
    reasons = []

    # Mood — categorical binary match
    user_mood = user_prefs.get("favorite_mood", "")
    if song["mood"] == user_mood:
        component = WEIGHTS["mood"] * 1.0
        score += component
        reasons.append(f"mood match: {song['mood']} (+{component:.2f})")
    else:
        reasons.append(f"mood mismatch: {song['mood']} vs {user_mood} (+0.00)")

    # Energy — continuous proximity
    user_energy = user_prefs.get("target_energy", 0.5)
    energy_gap = abs(user_energy - song["energy"])
    component = WEIGHTS["energy"] * (1 - energy_gap)
    score += component
    reasons.append(f"energy proximity: gap {energy_gap:.2f} (+{component:.2f})")

    # Acousticness — continuous proximity
    user_acousticness = user_prefs.get("target_acousticness", 0.5)
    acousticness_gap = abs(user_acousticness - song["acousticness"])
    component = WEIGHTS["acousticness"] * (1 - acousticness_gap)
    score += component
    reasons.append(f"acousticness proximity: gap {acousticness_gap:.2f} (+{component:.2f})")

    # Valence — continuous proximity
    user_valence = user_prefs.get("target_valence", 0.5)
    valence_gap = abs(user_valence - song["valence"])
    component = WEIGHTS["valence"] * (1 - valence_gap)
    score += component
    reasons.append(f"valence proximity: gap {valence_gap:.2f} (+{component:.2f})")

    # Danceability — continuous proximity
    user_danceability = user_prefs.get("target_danceability", 0.5)
    danceability_gap = abs(user_danceability - song["danceability"])
    component = WEIGHTS["danceability"] * (1 - danceability_gap)
    score += component
    reasons.append(f"danceability proximity: gap {danceability_gap:.2f} (+{component:.2f})")

    # Tempo — normalize to 0–1 before computing proximity
    user_tempo_norm = (user_prefs.get("target_tempo_bpm", 120.0) - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)
    song_tempo_norm  = (song["tempo_bpm"] - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)
    tempo_gap = abs(user_tempo_norm - song_tempo_norm)
    component = WEIGHTS["tempo"] * (1 - tempo_gap)
    score += component
    reasons.append(f"tempo proximity: gap {tempo_gap:.2f} (normalized) (+{component:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Filter by genre, score every candidate, and return the top k sorted by score descending."""
    candidates = [song for song in songs if song["genre"] == user_prefs.get("favorite_genre", "")]

    scored = [
        (song, *score_song(user_prefs, song))
        for song in candidates
    ]

    scored.sort(key=lambda x: x[1], reverse=True)

    return [(song, score, "\n".join(reasons)) for song, score, reasons in scored[:k]]
