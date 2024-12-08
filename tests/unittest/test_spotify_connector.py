import unittest

from connectors.spotify.spotify_connector import SpotifyConnector


class TestConnector(unittest.TestCase):
    def setUp(self) -> None:
        self.connector = SpotifyConnector()

    def test_credentials(self):
        self.assertGreater(len(self.connector.client_id), 5)
        self.assertGreater(len(self.connector.client_secret), 5)
        self.assertGreater(len(self.connector.token_post_url), 5)

    def test_get_token(self):
        access_token_keys = ["access_token", "token_type", "expires_in"]
        access_token_dict = self.connector.get_token()
        self.assertIsNotNone(access_token_dict)
        self.assertTrue(list(access_token_dict.keys()) == access_token_keys)

    def test_get_artist_info(self):
        artist_info_keys = [
            "external_urls",
            "followers",
            "genres",
            "href",
            "id",
            "images",
            "name",
            "popularity",
            "type",
            "uri",
        ]
        test_artist_id = "3eVuump9qyK0YCQQo4mKbc"

        test_artist_name = "Barış Manço"
        test_artist_genre = "anadolu rock"

        artist_info = self.connector.get_artist_info(test_artist_id)

        self.assertEqual(artist_info["type"], "artist")
        self.assertEqual(artist_info_keys, list(artist_info.keys()))
        self.assertEqual(test_artist_name, artist_info["name"])
        self.assertIn(test_artist_genre, artist_info["genres"])
        self.assertGreater(artist_info["followers"]["total"], 1)
