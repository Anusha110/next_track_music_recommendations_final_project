from recommendations.models import SpotifyTrack
from rest_framework import serializers

# This file contains input serializers for the two APIs in the recommendations app.
class GetRecommendationsInputSerializer(serializers.Serializer):

    track_ids = serializers.ListField(
          child=serializers.CharField(max_length=255),
          required=False,
          allow_empty=True,
          default=list
      )
    
    genres = serializers.ListField(
        child=serializers.CharField(max_length=255),
        required=False,
        allow_empty=True,
        default=list
    )

    mood = serializers.CharField(max_length=30, required=True)
    start_year = serializers.IntegerField(required=True)
    end_year = serializers.IntegerField(required=True)

    def validate(self, data):
        if not data.get("mood"):
            raise serializers.ValidationError("Mood is required")

        if not data.get("mood") in ["happy", "neutral", "sad"]:
            raise serializers.ValidationError("Mood is invalid, should be happy, neutral or sad")
        
        if not data.get("start_year"):
            raise serializers.ValidationError("Start year is required")
        if not data.get("end_year"):
            raise serializers.ValidationError("End year is required")

        if data.get("end_year") < data.get("start_year"):
            raise serializers.ValidationError("End year must be greater than or equal to start year")
        
        return data


class SearchTracksInputSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=100, required=True)

    def validate(self, data):
        if not data.get("query"):
            raise serializers.ValidationError("Query is required")
        return data