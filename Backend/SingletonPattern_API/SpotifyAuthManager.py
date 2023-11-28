import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import url_for

class SpotifyAuthManager():

  _instance = None; 

  def __new__(cls, *args, **kwargs): 
        if not cls._instance: 
            cls._instance = super(SpotifyAuthManager, cls).__new__(cls)
            cls._instance.spotify_oauth = cls._instance.create_spotify_oauth()
        return cls._instance

  def create_spotify_oauth(self):
      return SpotifyOAuth(
          client_id="f96ffd1f60e443c5b6b12adeb2863384",
          client_secret="101af488cb71478b8093a7d6311ae74d",
          redirect_uri=url_for('redirect_page', _external=True),
          scope='user-library-read playlist-modify-public playlist-modify-private'
      )
