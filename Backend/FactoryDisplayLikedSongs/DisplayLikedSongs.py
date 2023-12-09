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
  def __init__(self, token_info):
    self.token_info = token_info
    sp = spotipy.Spotify(auth=self.token_info['access_token'])
    self.tracks_info = self._get_tracks_info(sp)

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