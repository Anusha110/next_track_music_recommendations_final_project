import argparse
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_DATABASE_PATH = BASE_DIR / "db.sqlite3"
SOURCE_TABLE = "recommendations_spotifytrack"
EMBEDDING_TABLE = "recommendations_spotifytrackembedding"

FEATURE_COLUMNS = [
    "danceability",
    "energy",
    "loudness",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo"
]

CLIPPED_FEATURES = {
    # Tempo and duration can have long tails that make ordinary songs look too similar
    # after min-max scaling. Clipping keeps extreme metadata from dominating the vector.
    "tempo": (60.0, 200.0),
    "duration_ms": (30_000.0, 600_000.0),
}


def _clipped_expression(column):
    if column not in CLIPPED_FEATURES:
        return column

    lower, upper = CLIPPED_FEATURES[column]
    return f"""
        CASE
            WHEN {column} < {lower} THEN {lower}
            WHEN {column} > {upper} THEN {upper}
            ELSE {column}
        END
    """


def _normalization_stats(connection):

    # Get the min and max values for each column, to perform min-max scaling.
    
    stats = {}
    for column in FEATURE_COLUMNS:
        expr = _clipped_expression(column)
        row = connection.execute(
            f"SELECT MIN({expr}), MAX({expr}) FROM {SOURCE_TABLE} WHERE {column} IS NOT NULL"
        ).fetchone()
        stats[column] = row
    return stats


def _norm_sql(column, stats):

    # Performing min max normalization on the fly is slow, so we do it once and
    # store the results in the database. This is a one-time operation.
    
    min_value, max_value = stats[column]
    expr = _clipped_expression(column)

    if min_value is None or max_value is None or min_value == max_value:
        return "0.0"

    return f"(({expr}) - {float(min_value)}) / ({float(max_value)} - {float(min_value)})"


def rebuild_embeddings(database_path=DEFAULT_DATABASE_PATH):
    with sqlite3.connect(database_path) as connection:
        stats = _normalization_stats(connection)
        connection.execute(f"DELETE FROM {EMBEDDING_TABLE}")

        normalized_columns = [
            f"{_norm_sql(column, stats)} AS {column}_norm"
            for column in FEATURE_COLUMNS
        ]

        connection.execute(
            f"""
            INSERT INTO {EMBEDDING_TABLE} (
                track_id,
                danceability_norm,   
                energy_norm,
                loudness_norm,
                mode_norm,
                speechiness_norm,
                acousticness_norm,
                instrumentalness_norm,
                liveness_norm,
                valence_norm,
                tempo_norm
            )
            SELECT
                track_id,
                {", ".join(normalized_columns)}
            FROM {SOURCE_TABLE}
            WHERE track_id IS NOT NULL
            """
        )
        count = connection.execute(f"SELECT COUNT(*) FROM {EMBEDDING_TABLE}").fetchone()[0]

    return count


def parse_args():
    parser = argparse.ArgumentParser(
        description="Build normalized Spotify audio feature embeddings in SQLite."
    )
    parser.add_argument("--database", default=DEFAULT_DATABASE_PATH, type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    row_count = rebuild_embeddings(args.database)
    print(f"Rebuilt {EMBEDDING_TABLE} with {row_count:,} rows")
