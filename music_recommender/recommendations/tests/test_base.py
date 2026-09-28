
from rest_framework.test import APIClient
from django.test import TestCase
from .factories import SpotifyTrackFactory, MusicBrainzArtistTagFactory, SpotifyTrackEmbeddingFactory

# This is a resuable base class for all tests in the recommendation app

class APITestBase(TestCase):

    def setUp(self):
        self.client = APIClient()
        # high tempo songs
        self.tracks = SpotifyTrackFactory.create_batch(20, year=2005, genre='pop', tempo=180, valence=0.8, energy=0.7,
                                                        danceability=0.9, loudness=0.5, speechiness=0.4, acousticness=0.3, instrumentalness=0.2, liveness=0.1)

        # low tempo songs
        self.tracks.extend(SpotifyTrackFactory.create_batch(20, year=2005, genre='pop', tempo=65, valence=0.1, energy=0.7,
                                                        danceability=0.2, loudness=0.5, speechiness=0.4, acousticness=0.3, instrumentalness=0.2, liveness=0.1))

        # medium tempo songs
        self.tracks.extend(SpotifyTrackFactory.create_batch(5, year=2005, genre='pop', tempo=100, valence=0.5, energy=0.7,
                                                                danceability=0.5, loudness=0.5, speechiness=0.4, acousticness=0.3, instrumentalness=0.2, liveness=0.1))
        self.embeddings = []
        self.artists = []
        self.tags = []
        self.track_id_wise_track = {}

        for each in self.tracks:
            self.embeddings.append(SpotifyTrackEmbeddingFactory(track=each))
            self.artists.append(each.artist)
            self.tags.append(MusicBrainzArtistTagFactory(artist=each.artist))
            self.track_id_wise_track[each.track_id] = each
