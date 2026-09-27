import os, sys
import django
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "music_recommender.settings")
django.setup()

from recommendations.models import MusicBrainzArtist, SpotifyTrack
import sqlite3
from collections import defaultdict
import time

BULK_SIZE = 4000

def process_batch(artist_name_wise_track_ids):
    all_spotify_artist_names = list(artist_name_wise_track_ids.keys())
    if not all_spotify_artist_names:
        return

    placeholders = ", ".join("?" for _ in all_spotify_artist_names)

    # Fetch artists from MusicBrainz
    cursor.execute(
        f"SELECT artist.id, artist.name, artist.gid FROM artist "
        f"WHERE artist.name IN ({placeholders})",
        all_spotify_artist_names,
    )
    fetched_artists = cursor.fetchall()

    records = []
    for fetched_artist in fetched_artists:
        records.append(
            MusicBrainzArtist(
                id=fetched_artist[0],
                artist_name=fetched_artist[1],
                music_brainz_id=fetched_artist[2],
            )
        )

    # Bulk create artists
    MusicBrainzArtist.objects.bulk_create(
        records,
        update_conflicts=True,
        unique_fields=["id"],
        update_fields=["artist_name", "music_brainz_id"],
        batch_size=BULK_SIZE,
    )

    # Update Spotify Data Artist Foreign Key
    for artist_id, artist_name, _ in fetched_artists:
        track_ids = artist_name_wise_track_ids[artist_name]
        SpotifyTrack.objects.filter(track_id__in=track_ids).update(artist=artist_id)


# Connect the local music brainz db
connection = sqlite3.connect(PROJECT_ROOT / "music_brainz_db")
cursor = connection.cursor()

# Get all Spotify Track IDs and Artist Names
#   - Iterate over the Spotify Tracks in bulks of 4000 tracks. (.iterator(chunk_size=000))
spotify_tracks = SpotifyTrack.objects.values_list(
    "track_id", "artist_name"
).iterator(chunk_size=BULK_SIZE)

bulk_count = 0
artist_name_wise_track_ids = defaultdict(list)
start_time = time.time()
print("Starting Time: ", start_time)


for track_id, artist_name in spotify_tracks:
    artist_name_wise_track_ids[artist_name].append(track_id)
    bulk_count += 1

    # Process every full batch to avoid excessive memory use.
    if bulk_count % BULK_SIZE == 0:
        process_batch(artist_name_wise_track_ids)
        artist_name_wise_track_ids = defaultdict(list)
        print("Completed processing 4000 tracks, batch_no: ", bulk_count / BULK_SIZE)
        print("Total time taken: ", time.time() - start_time)

# Process the final partial batch as well.
process_batch(artist_name_wise_track_ids)
