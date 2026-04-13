"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


PROFILES = {
    "High-Energy Pop": {
        "favorite_genre":      "pop",
        "favorite_mood":       "happy",
        "target_energy":       0.9,
        "target_acousticness": 0.15,
        "target_valence":      0.6,
        "target_danceability": 0.9,
        "target_tempo_bpm":    100,
    },
    "Chill Lofi": {
        "favorite_genre":      "lofi",
        "favorite_mood":       "chill",
        "target_energy":       0.38,
        "target_acousticness": 0.80,
        "target_valence":      0.58,
        "target_danceability": 0.60,
        "target_tempo_bpm":    75,
    },
    "Deep Intense Rock": {
        "favorite_genre":      "rock",
        "favorite_mood":       "intense",
        "target_energy":       0.95,
        "target_acousticness": 0.08,
        "target_valence":      0.40,
        "target_danceability": 0.65,
        "target_tempo_bpm":    155,
    },
}


EDGE_CASES = {
    # High energy but sad mood — soul only has one sad song (energy 0.38).
    # Does high energy target override the mood match, or does mood win?
    "Conflicting Energy + Mood (soul/sad/energy 0.9)": {
        "favorite_genre":      "soul",
        "favorite_mood":       "sad",
        "target_energy":       0.9,
        "target_acousticness": 0.40,
        "target_valence":      0.30,
        "target_danceability": 0.50,
        "target_tempo_bpm":    72,
    },
    # Genre that does not exist in the catalog.
    # Should return zero results — tests that the hard filter doesn't crash.
    "Ghost Genre (blues)": {
        "favorite_genre":      "blues",
        "favorite_mood":       "sad",
        "target_energy":       0.5,
        "target_acousticness": 0.5,
        "target_valence":      0.5,
        "target_danceability": 0.5,
        "target_tempo_bpm":    90,
    },
    # All targets at exactly 0.5 — the perfectly neutral listener.
    # Every song scores similarly; reveals whether any bias exists in the weights.
    "Perfectly Neutral (pop/happy/all 0.5)": {
        "favorite_genre":      "pop",
        "favorite_mood":       "happy",
        "target_energy":       0.5,
        "target_acousticness": 0.5,
        "target_valence":      0.5,
        "target_danceability": 0.5,
        "target_tempo_bpm":    120,
    },
    # Wants lofi genre but targets energy and acousticness that no lofi song has.
    # All lofi songs are low energy and high acoustic — the opposite of these targets.
    "Impossible Lofi (high energy, low acoustic)": {
        "favorite_genre":      "lofi",
        "favorite_mood":       "focused",
        "target_energy":       0.95,
        "target_acousticness": 0.05,
        "target_valence":      0.90,
        "target_danceability": 0.95,
        "target_tempo_bpm":    160,
    },
    # Jazz only has one song with mood "relaxed" — requesting "angry" guarantees
    # zero mood matches. Does the system still return something reasonable?
    "Mood With No Match in Genre (jazz/angry)": {
        "favorite_genre":      "jazz",
        "favorite_mood":       "angry",
        "target_energy":       0.85,
        "target_acousticness": 0.20,
        "target_valence":      0.30,
        "target_danceability": 0.70,
        "target_tempo_bpm":    130,
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for profile_name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\n" + "=" * 50)
        print(f"  {profile_name.upper()}")
        print("=" * 50)

        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n#{rank}  {song['title']} by {song['artist']}")
            print(f"    Genre: {song['genre']}  |  Mood: {song['mood']}")
            print(f"    Final Score: {score:.2f}")
            print("    Breakdown:")
            for line in explanation.split("\n"):
                print(f"      - {line}")
            print("    " + "-" * 44)

        print()

    print("\n" + "#" * 50)
    print("  EDGE CASE TESTS")
    print("#" * 50)

    for profile_name, user_prefs in EDGE_CASES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\n" + "=" * 50)
        print(f"  {profile_name.upper()}")
        print("=" * 50)

        if not recommendations:
            print("\n  [No results — genre not found in catalog]\n")
            continue

        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n#{rank}  {song['title']} by {song['artist']}")
            print(f"    Genre: {song['genre']}  |  Mood: {song['mood']}")
            print(f"    Final Score: {score:.2f}")
            print("    Breakdown:")
            for line in explanation.split("\n"):
                print(f"      - {line}")
            print("    " + "-" * 44)

        print()


if __name__ == "__main__":
    main()
