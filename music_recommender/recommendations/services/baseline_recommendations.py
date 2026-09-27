from typing import Any, Dict, Iterable, List
from collections import defaultdict
from recommendations.models import SpotifyTrack, SpotifyTrackEmbedding, MusicBrainzArtistTag
from .tag_overlap_score import TagOverlapScoreService
from .mood_score import MoodScoreService
from django.db.models import Q
import math
from .playlist_recommendations import PlaylistRecommendationService

CANDIDATE_LIMIT = 5000
EMBEDDING_FIELDS = [
    "danceability_norm",
    "energy_norm",
    "loudness_norm",
    "mode_norm",
    "speechiness_norm",
    "acousticness_norm",
    "instrumentalness_norm",
    "liveness_norm",
    "valence_norm",
    "tempo_norm",
]

# This is not used in production. It was used during user evaluation only for baseline comparison.
# It does not consider simliarity scores at all, and simply filters tracks based on genre, year, and mood.

class BaselinePlaylistRecommendationService:

    def get_recommended_playlist(
        self,
        track_ids: List[str],
        user_preferences: str | Dict[str, Any],
    ):  

        playlist_service = PlaylistRecommendationService()
        excluded_track_ids = track_ids or []

        # Parse user_preferences and set filters.
        user_preferences = playlist_service._parse_preferences(user_preferences)
        mood = str(user_preferences.get("mood", "")).lower()
        filters = playlist_service._create_genre_year_filters(user_preferences)

        # Set track ordering
        fallback_order_by = ["mood_score", "-popularity", "track_name"]
        if mood == "happy":
            fallback_order_by = ["-mood_score", "-popularity", "track_name"]

        # Filter all tracks based on genre, year, and MOOD score, and get Candidates.
        # First 5000 Tracks are considered in the candidate pool.
        candidates = list(
            playlist_service._filter_mood(SpotifyTrack.objects, mood)
            .filter(filters)
            .exclude(track_id__in=excluded_track_ids)  # Exclude seed track ids.
            .order_by(*fallback_order_by)[:CANDIDATE_LIMIT]
        )
   
        return [
            playlist_service._track_payload_with_similarity(track, None)
            for track in candidates[:10]
        ]

