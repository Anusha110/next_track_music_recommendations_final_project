import factory
from recommendations.models import SpotifyTrack, MusicBrainzArtistTag, MusicBrainzArtist, SpotifyTrackEmbedding


# This file contains a factory for every models in the recommendations app.

class MusicBrainzArtistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MusicBrainzArtist
        
    id = factory.Sequence(lambda n: n+1000)
    artist_name = factory.Sequence(lambda n: f'artist{n}')
    music_brainz_id = factory.Faker('uuid4')

class SpotifyTrackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SpotifyTrack
        
    track_id = factory.Sequence(lambda n: f'track{n}')
    artist_name = factory.Sequence(lambda n: f'artist{n}')
    track_name = factory.Sequence(lambda n: f'track{n}')
    artist = factory.SubFactory(MusicBrainzArtistFactory)
    popularity = factory.Faker('random_int', min=0, max=100)
    year = factory.Faker('pyint', min_value=1970, max_value=2024)

    _GENRE_CHOICES = ['pop', 'rock', 'hiphop']

    genre = factory.Faker('random_element', elements=_GENRE_CHOICES)
    danceability = factory.Faker('pyfloat', left_digits=2, right_digits=2, min_value=0, max_value=1)
    energy = factory.Faker('pyfloat', left_digits=2, right_digits=2 , min_value=0, max_value=1)
    key = factory.Faker('pyint', min_value=0, max_value=10)
    loudness = factory.Faker('pyfloat', left_digits=2, right_digits=2,  min_value=0, max_value=1)
    mode = factory.Faker('pyint', min_value=0, max_value=10)
    speechiness = factory.Faker('pyfloat', left_digits=2, right_digits=2,  min_value=0, max_value=1)
    acousticness = factory.Faker('pyfloat', left_digits=2, right_digits=2,  min_value=0, max_value=1)
    instrumentalness = factory.Faker('pyfloat', left_digits=2, right_digits=2,  min_value=0, max_value=1)
    liveness = factory.Faker('pyfloat', left_digits=2, right_digits=2, min_value=0, max_value=1)
    valence = factory.Faker('pyfloat', left_digits=2, right_digits=2, min_value=0, max_value=1)
    tempo = factory.Faker('pyfloat', left_digits=2, right_digits=2, min_value=0, max_value=1)
    duration_ms = factory.Faker('pyint', min_value=0, max_value=10000)
    time_signature = factory.Faker('pyint', min_value=0, max_value=10)

    artist = factory.SubFactory(MusicBrainzArtistFactory)
    

class MusicBrainzArtistTagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MusicBrainzArtistTag
        
    artist = factory.SubFactory(MusicBrainzArtistFactory)
    tag_id = factory.Sequence(lambda n: n)
    tag_name = factory.Sequence(lambda n: f'tag{n}')
    tag_count = factory.Sequence(lambda n: n)

class SpotifyTrackEmbeddingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SpotifyTrackEmbedding
        
    track = factory.SubFactory(SpotifyTrackFactory)
    danceability_norm = factory.Sequence(lambda n: n)
    energy_norm = factory.Sequence(lambda n: n)
    loudness_norm = factory.Sequence(lambda n: n)
    mode_norm = factory.Sequence(lambda n: n)
    speechiness_norm = factory.Sequence(lambda n: n)
    acousticness_norm = factory.Sequence(lambda n: n)
    instrumentalness_norm = factory.Sequence(lambda n: n)
    liveness_norm = factory.Sequence(lambda n: n)    
    valence_norm = factory.Sequence(lambda n: n)
    tempo_norm = factory.Sequence(lambda n: n)
