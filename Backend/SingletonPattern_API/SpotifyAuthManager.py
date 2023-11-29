import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import url_for


class SpotifyAuthManager():

  _instance = None; 

  #it has to be new so that only one instance of the class exists 
  def __new__(cls, *args, **kwargs): #cls is the class itself, *args and **kwargs collect any additional keywords that can be used to instatiate the class 
        if not cls._instance: #if there is no instance 
            cls._instance = super(SpotifyAuthManager, cls).__new__(cls) #creates a new instance with the keyword super 
            cls._instance.spotify_oauth = cls._instance.create_spotify_oauth() #inits the aclyal argument 
        return cls._instance #returns the instance 

  def create_spotify_oauth(self):
      return SpotifyOAuth(
          client_id="f96ffd1f60e443c5b6b12adeb2863384",
          client_secret="101af488cb71478b8093a7d6311ae74d",
          redirect_uri=url_for('redirect_page', _external=True),
          scope='user-library-read playlist-modify-public playlist-modify-private'
      )
