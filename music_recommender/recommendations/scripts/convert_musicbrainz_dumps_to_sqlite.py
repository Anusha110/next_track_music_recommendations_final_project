
import os
import sqlite3
from pathlib import Path

import pandas as pd

## Convert MusicBrainz tab-separated dumps to a SQLite database

BASE_DIR = Path(__file__).resolve().parents[2]
project_path = Path(
    os.environ.get("MUSIC_BRAINZ_DATA_PATH", BASE_DIR / "music_brainz_mini")
)

music_brainz_db_name = BASE_DIR / "music_brainz_db"

conn = sqlite3.connect(music_brainz_db_name)

artist_df = pd.read_csv(project_path / 'artist', sep='\t', header=None)

artist_df.columns = [
    "id",
    "gid",
    "name",
    "sort_name",
    "begin_date_year",
    "begin_date_month",
    "begin_date_day",
    "end_date_year",
    "end_date_month",
    "end_date_day",
    "type",
    "area",
    "gender",
    "comment",
    "edits_pending",
    "last_updated",
    "ended",
    "begin_area",
    "end_area"
]

artist_df.to_sql(
    'artist',
    conn,
    if_exists="replace",
    index=False
)


## Convert Artist Tag dump to SQLITE DB

artist_tag_df = pd.read_csv(
    project_path / 'artist_tag', sep='\t', header=None)


artist_tag_df.columns = [
    "artist_id",
    "tag_id",
    "count",
    "last_updated"
]

artist_tag_df.to_sql(
    'artist_tag',
    conn,
    if_exists="replace",
    index=False
)

## Convert Tag dump to SQLITE DB

tag_df = pd.read_csv(project_path / 'tag', sep='\t', header=None)

tag_df.columns = [
    "id",
    "name",
    "ref_count"
]

tag_df.to_sql(
    'tag',
    conn,
    if_exists="replace",
    index=False
)
