import os, sys
import django
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "music_recommender.settings")
django.setup()

from recommendations.models import MusicBrainzArtist, MusicBrainzArtistTag
import sqlite3



# Connect the local music brainz db
connection = sqlite3.connect(PROJECT_ROOT / "music_brainz_db")
cursor = connection.cursor()


# Get all MusicBrainz Artist IDs
music_brainz_artist_ids = list(MusicBrainzArtist.objects.values_list("id", flat=True))

created_artist_tags = 0

# SQLite has a limit on the number of parameters in one query, so process
# artist IDs in batches.
for start in range(0, len(music_brainz_artist_ids), 500):
    artist_ids = music_brainz_artist_ids[start:start + 500]
    artist_id_placeholders = ", ".join("?" for _ in artist_ids)

    cursor.execute(
        f"SELECT artist_tag.tag_id, artist_tag.artist_id, tag.name, artist_tag.count "
        f"FROM artist_tag INNER JOIN tag ON artist_tag.tag_id = tag.id "
        f"WHERE artist_tag.artist_id IN ({artist_id_placeholders})",
        artist_ids,
    )
    tag_records = [
        MusicBrainzArtistTag(
            tag_id=tag_id,
            artist_id=artist_id,
            tag_name=tag_name,
            tag_count=tag_count,
        )
        for tag_id, artist_id, tag_name, tag_count in cursor.fetchall()
    ]

    MusicBrainzArtistTag.objects.bulk_create(
        tag_records,
        batch_size=2000,
        update_conflicts=True,
        unique_fields=["artist", "tag_id"],
        update_fields=["tag_name", "tag_count"],
    )
    created_artist_tags += len(tag_records)

print("created_artist_tags count: ", created_artist_tags)
