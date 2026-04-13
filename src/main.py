"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    user_prefs = {
        "favorite_genre":      "pop",
        "favorite_mood":       "happy",
        "target_energy":       0.9,
        "target_acousticness": 0.15,
        "target_valence":      0.6,
        "target_danceability": 0.9,
        "target_tempo_bpm":    100,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 50)
    print("  TOP RECOMMENDATIONS")
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


if __name__ == "__main__":
    main()
