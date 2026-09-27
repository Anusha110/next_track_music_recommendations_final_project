from .test_base import APITestBase


# This class tests the playlist recommendation API.
# It tests both success and failures cases providing a good test suite.

class PlaylistRecommendationAPITests(APITestBase):


    def test_recommendations_return_ten_tracks_and_200_status_code(self):

        track_ids = list(self.track_id_wise_track.keys())

        responses = self.client.post('', {
                               'track_ids': track_ids[2:4],

             "genres": ["rock", "pop"],
             "mood": "happy",
             "start_year": 2000,
             "end_year": 2020,
        }, format='json')

        self.assertEqual(responses.status_code, 200)
        self.assertLessEqual(len(responses.data), 10)

    def test_recommendations_returns_tracks_with_correct_genre(self):

            track_ids = list(self.track_id_wise_track.keys())

            input_genres = ["rock", "pop"]
            responses = self.client.post('', {
                                       'track_ids': track_ids[2:4],

                     "genres": ["pop", "rock"],
                     "mood": "happy",
                     "start_year": 2000,
                     "end_year": 2020,
                }, format='json')

            self.assertEqual(responses.status_code, 200)

            for each in responses.data:
                self.assertIn(each['genre'], input_genres)

    def test_recommendations_returns_tracks_with_correct_year(self):

        track_ids = list(self.track_id_wise_track.keys())

        valid_year_range = [2000, 2001, 2002, 2003, 2004, 2005]

        responses = self.client.post('', {
                                   'track_ids': track_ids[2:4],

                    "genres": ["rock", "pop"],
                    "mood": "happy",
                    "start_year": 2000,
                    "end_year": 2005,
            }, format='json')

        self.assertEqual(responses.status_code, 200)

        for each in responses.data:
            self.assertIn(each['year'], valid_year_range)

    def test_recommendations_returns_tracks_with_correct_mood(self):
        track_ids = list(self.track_id_wise_track.keys())

        responses = self.client.post('', {
                                       'track_ids': track_ids[2:4],

                        "genres": ["rock", "pop"],
                        "mood": "happy",
                        "start_year": 2000,
                        "end_year": 2005,
                }, format='json')

        for each in responses.data:
            track = self.track_id_wise_track[each['track_id']]
            if track.tempo < 60.0:
                tempo_norm = 0.0
            elif track.tempo > 200.0:
                tempo_norm = 1.0
            else:
                tempo_norm = (track.tempo - 60.0) / 140.0 # 200.0 - 60.0
                 
            mood_score = tempo_norm + track.danceability + track.valence/3
            self.assertGreater(mood_score, 0.6)

    def test_recommendations_returns_tracks_with_sad_mood(self):

        track_ids = list(self.track_id_wise_track.keys())

        responses = self.client.post('', {
                                       'track_ids': track_ids[2:4],

                        "genres": ["rock", "pop"],
                        "mood": "sad",
                        "start_year": 2000,
                        "end_year": 2005,
                }, format='json')

        for each in responses.data:

            track = self.track_id_wise_track[each['track_id']]
            if track.tempo < 60.0:
                tempo_norm = 0.0
            elif track.tempo > 200.0:
                tempo_norm = 1.0
            else:
                tempo_norm = (track.tempo - 60.0) / 140.0 # 200.0 - 60.0


            mood_score = ((tempo_norm + track.danceability + track.valence)/3)
            self.assertLess(mood_score, 0.4)

    
    def test_recommendations_returns_tracks_with_neutral_mood(self):
        track_ids = list(self.track_id_wise_track.keys())

        
        responses = self.client.post('', {
                                       'track_ids': track_ids[2:4],

                        "genres": ["rock", "pop"],
                        "mood": "neutral",
                        "start_year": 2000,
                        "end_year": 2005,
                }, format='json')

        for each in responses.data:

            track = self.track_id_wise_track[each['track_id']]
            if track.tempo < 60.0:
                tempo_norm = 0.0
            elif track.tempo > 200.0:
                tempo_norm = 1.0
            else:
                tempo_norm = (track.tempo - 60.0) / 140.0 # 200.0 - 60.0
            
            mood_score = tempo_norm + track.danceability + track.valence/3

            self.assertGreaterEqual(mood_score, 0.4)
            self.assertLessEqual(mood_score, 0.7)

    def test_recommendations_returns_tracks_in_descending_order_of_similarity(self):

        track_ids = list(self.track_id_wise_track.keys())

        responses = self.client.post('', {
                    'track_ids': track_ids[2:4],
                        "genres": ["rock", "pop"],
                        "mood": "happy",
                        "start_year": 2000,
                        "end_year": 2005,
                }, format='json')

        self.assertEqual(responses.status_code, 200)
        sorted_list = sorted(responses.data, key=lambda x: x['similarity_score'], reverse=True)
        self.assertEqual(sorted_list, responses.data)

    def test_recommendations_returns_handle_missing_embeddings(self):
   
        track_ids = list(self.track_id_wise_track.keys())

        for each in self.embeddings:
            if each.track_id in track_ids[2:4]:
                pass

            each.delete()

        responses = self.client.post('', {
                    'track_ids': track_ids[2:4],
                        "genres": ["rock", "pop"],
                        "mood": "happy",
                        "start_year": 2000,
                        "end_year": 2005,
                }, format='json')

        self.assertEqual(responses.status_code, 200)


    def test_empty_mood_returns_400_status_code(self):
        track_ids = list(self.track_id_wise_track.keys())

        responses = self.client.post('', {
                    'track_ids': track_ids[2:4],

                     "genres": ["pop", "rock"],
                     "mood": "",
                     "start_year": 2000,
                     "end_year": 2020,
                }, format='json')

        self.assertEqual(responses.status_code, 400)

    def test_invalid_mood_returns_400_status_code(self):
        track_ids = list(self.track_id_wise_track.keys())

        responses = self.client.post('', {
                    'track_ids': track_ids[2:4],

                     "genres": ["pop", "rock"],
                     "mood": "random",
                     "start_year": 2000,
                     "end_year": 2020,
                }, format='json')

        self.assertEqual(responses.status_code, 400)

    def test_missing_start_year_returns_400_status_code(self):
        track_ids = list(self.track_id_wise_track.keys())

        responses = self.client.post('', {
                    'track_ids': track_ids[2:4],

                     "genres": ["pop", "rock"],
                     "mood": "happy",
                     "end_year": 2020,
                }, format='json')

        self.assertEqual(responses.status_code, 400)

    def test_missing_end_year_returns_400_status_code(self):
        track_ids = list(self.track_id_wise_track.keys())

        responses = self.client.post('', {
                    'track_ids': track_ids[2:4],

                     "genres": ["pop", "rock"],
                     "mood": "happy",
                     "start_year": 2000,
                }, format='json')

        self.assertEqual(responses.status_code, 400)



    