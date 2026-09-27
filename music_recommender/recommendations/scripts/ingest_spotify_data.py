import argparse
import os
import sys
from pathlib import Path

import django

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "music_recommender.settings")
django.setup()

from recommendations.models import SpotifyTrack
from recommendations.scripts.clean_spotify_data import clean_spotify_data


MODEL_COLUMNS = [
    "serial_number", "artist_name", "track_name", "track_id", "popularity",
    "year", "genre", "danceability", "energy", "key", "loudness", "mode",
    "speechiness", "acousticness", "instrumentalness", "liveness", "valence",
    "tempo", "duration_ms", "time_signature",
]


def ingest_spotify_data(input_path, cleaned_output_path):
    dataframe = clean_spotify_data(input_path, cleaned_output_path)
    dataframe["genre"] = dataframe["genre"].fillna("")
    records = [
        SpotifyTrack(**row)
        for row in dataframe[MODEL_COLUMNS].to_dict(orient="records")
    ]
    SpotifyTrack.objects.bulk_create(
        records,
        batch_size=2000,
        update_conflicts=True,
        unique_fields=["track_id"],
        update_fields=[column for column in MODEL_COLUMNS if column != "track_id"],
    )
    return len(records)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Clean and load Spotify tracks into the Django database."
    )
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument(
        "--cleaned-output",
        default=PROJECT_ROOT / "spotify_data_cleaned.csv",
        type=Path,
    )
    args = parser.parse_args()
    count = ingest_spotify_data(args.input, args.cleaned_output)
    print(f"Loaded {count:,} Spotify tracks")
