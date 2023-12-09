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
  def __init__(self,token_info ,  *args, **kwargs):
      self.liked_songs = spotipy.Spotify(auth=token_info['access_token']).current_user_saved_tracks()
      self.tracks = []
      for offset in range(0, 1000, 50):
        response = spotipy.Spotify(auth=token_info['access_token']).current_user_saved_tracks(limit = 50, offset=offset)
        if len(response) == 0: # type: ignore
          break
        self.tracks.extend(response.get('items', [])) # type: ignore
      self.tracks_info = []
      for item in self.tracks:
        track_info = {}
        track_info['name'] = item['track']['name']
        names = "" + item['track']['artists'][0]['name']
        for person in item['track']['artists'][1:-1]:
          names+= ", " + person['name']
        track_info["artists"] = names
        track_info['id'] = item['track']['id']
        self.tracks_info.append(track_info)

  def get_info(self): 
    return self.tracks_info
