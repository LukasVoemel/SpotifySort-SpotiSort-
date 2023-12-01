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
      
     
      self.sp = spotipy.Spotify(auth=token_info['access_token'])
      self.liked_songs = self.sp.current_user_saved_tracks()
      self.tracks = []
      limit_step = 50
      for offset in range(0, 1000, limit_step):
        response = self.sp.current_user_saved_tracks(limit = limit_step, offset=offset)
        #print(response)
        if len(response) == 0:
          break
        self.tracks.extend(response.get('items', []))
        
      self.tracks_info = []
      #print("ASdfasdf   ", self.tracks[0])
      for item in self.tracks:
        track_info = {}
        track = item['track']
        track_info['name'] = track['name']
        self.tracks_info.append(track_info)


  def get_info(self): 
    return self.tracks_info
