from flask import session, redirect, url_for
from abc import ABC, abstractmethod
from SingeltonAppManager.AppManager import app
import spotipy

#Product Interface
class SongInfo(ABC):
    @abstractmethod
    def get_info(self):
        pass

# Concrete Product: Artist
class ArtistInfo(SongInfo):
<<<<<<< HEAD
  def __init__(self,token_info ,  *args, **kwargs):
      
     
      self.sp = spotipy.Spotify(auth=token_info['access_token'])
      self.liked_songs = self.sp.current_user_saved_tracks()
      self.tracks = []
      limit_step = 50
      for offset in range(0, 1000, limit_step):
        response = self.sp.current_user_saved_tracks(limit = limit_step, offset=offset)
        print(response)
        if len(response) == 0:
          break
        self.tracks.extend(response.get('items', []))
        
      self.tracks_info = []
      
      for item in self.tracks:
        track_info = {}
        track = item['track']
        artists = track['artists']
        track_info['name'] = track['name']
        names = "" + artists[0]['name']
        for person in artists[1:-1]:
          names+= ", " + person['name']
        track_info["artists"] = names
        self.tracks_info.append(track_info)
=======
  def __init__(self, token_info):
    self.token_info = token_info
    sp = spotipy.Spotify(auth=self.token_info['access_token'])
    self.tracks_info = self._get_tracks_info(sp)
>>>>>>> bce0f7f1cea1a5070e08cd447e175c2e3ccee647

  def _get_tracks_info(self,sp):
    tracks = []
    for offset in range(0, 1000, 50):
      response = sp.current_user_saved_tracks(limit = 50, offset=offset)
      if len(response) == 0: # type: ignore
        break
      tracks.extend(response.get('items', [])) # type: ignore
    tracks_info = []
    for item in tracks:
      track_info = {
        'name': item['track']['name'],
        'artists': ", ".join(artist['name'] for artist in item['track']['artists']),
        'id': item['track']['id']
      }
      tracks_info.append(track_info)
    return tracks_info

  def get_info(self): 
    return self.tracks_info

class InfoFactory(ABC):
    @abstractmethod
    def create_song_info(self, token_info):
        pass

# Concrete Factory: ArtistInfo
class ArtistInfoFactory(InfoFactory):
    def create_song_info(self, token_info):
        return ArtistInfo(token_info)