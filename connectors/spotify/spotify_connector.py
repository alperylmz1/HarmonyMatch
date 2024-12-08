import os
import requests
import json

from dotenv import load_dotenv


class SpotifyConnector:
    def __init__(self):
        self._load_credentials()

    def _load_credentials(self) -> None:
        """
        Fetching credentials from .env file. This credentials are mandatory to get access token from Spotify.

        Parameters
            None

        Returns
            None
        """

        load_dotenv(os.path.abspath("config/credentials.env"))
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.token_post_url = os.getenv("TOKEN_POST_URL")

    def get_token(self) -> dict:
        """
        This function performs post request with CLIENT_ID and CLIENT_SECRET in body, under -data.

        Headers is also defined and will stay same.

        Parameters
            None

        Returns
            dict:ACCESS_TOKEN: This token will be used in further API requests, i.e. getting artist info. Expires in 1 hour.
            Has 3 keys: "access_token", "token_type", "expires_in"
        """

        result = requests.post(
            url=self.token_post_url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
        )

        return json.loads(result.content)

    def get_artist_info(self, artist_id: str) -> dict:
        """
        This function performs post request to fetch information about artist we indicates with artist_id. Access token used, where we fetched in get_token function.
        Headers will be same for all of the Spotify endpoints. The url will change regarding the api calls you perform. I.e. artist in url for this example.

        Parameters:
            str:artist_id: Unique ID of the artist we want to fetch information about.

        Returns:
            dict:Artist_Info: This dictionary has 10 keys and holding informations about given artist.
            keys => ['external_urls', 'followers', 'genres', 'href', 'id', 'images', 'name', 'popularity', 'type', 'uri']
        """

        response = requests.get(
            url="https://api.spotify.com/v1/artists/" + artist_id,
            headers={"Authorization": "Bearer " + self.get_token()["access_token"]},
        )

        return json.loads(response.content)
