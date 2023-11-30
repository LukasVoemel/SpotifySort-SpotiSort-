from flask import session, redirect, url_for
from abc import ABC, abstractmethod
from SingeltonAppManager.AppManager import app
import spotipy

#Product Interface
class SongInfo(ABC):

  def get_info(self):
    pass

# Concrete Product: Artist
class ArtistInfo(SongInfo):
  def __init__(self, *args, **kwargs):
    try:
      from SingeltonAppManager.AppManager import TOKEN_INFO # Import the app instance for the token
      self.sp = spotipy.Spotify(auth=TOKEN_INFO['access_token'])
      self.liked_songs = self.sp.current_user_saved_tracks()
  
      self.tracks_info = []

      for item in self.liked_songs['items']:
        track_info = {}
        track = item['track']
        track_info['name'] = track['name']
        self.tracks_info.append(track_info)
      
    except Exception as e: 
      print("ERROR")


  def get_info(self): 
    return self.tracks_info
