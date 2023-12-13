from abc import ABC, abstractmethod
from SingeltonAppManager.AppManager import app
import spotipy
from ObserverTracks.ObserveLikedTracks import TracksSubject, trackInfoObserver
import time

#Product Interface
  # defines common interface for all objects (products)
  # that can we produced by the createor and subclasses 
  # SongInfo Class is the product interface that ensures that all types of songs 
  # information(artist, song, album) all implement the get_info method which provides standart for getting the data 

#Concerete Products 
  # Specifc implementeations of the prodcut interface 
  # each concerere product calss implements the interface in a way appropriate to its type 
  #ArtistInfo, SongInfo, AlbumInfo are concrete prodicys which provife specifc implementation 
  #

#Factory Interface
  # defines methods for creating objects, In the factory Pattern 
  # this interface allows for the creating ob objects 
  # without specifiuiong the exact class of the object that will be created 
  #info factory is the factory inerface 
  #declares methods like artist info, create song info, create almbum info, which are meant to be implemented by conrcrete factores to specify types of song info object 

#Concrete factoreis
  # impements factory interface and are responsbible for creating one of more types of concrete products 
  # each concrere producs knows how to make a concrete facotry 

#Product Interface
class SongInfo(ABC): # type: ignore
    @abstractmethod
    def get_info(self):
        pass

# Concrete Products: Artist
class ArtistInfo(SongInfo):
  def __init__(self, token_info):
    self.token_info = token_info
    self.sp = spotipy.Spotify(auth=self.token_info['access_token'])
    self.tracks_info = None
    self.subject = TracksSubject(self.sp)
    self.observer = trackInfoObserver()
    self.subject.register_observer(self.observer)
    self.subject.run()
    time.sleep(10)

  def get_info(self): 
    if self.tracks_info is None:
       self.tracks_info = self.observer.tracks

    artist_names = []
    first_item = self.tracks_info

    for item in first_item['items']: # type: ignore
      for artist in item['track']['artists']:
          artist_name = artist['name']
          artist_names.append(artist_name)
    
    return artist_names

class SongInfo(SongInfo):
  def __init__(self, token_info):
    self.token_info = token_info
    self.sp = spotipy.Spotify(auth=self.token_info['access_token'])
    self.tracks_info = None
    self.subject = TracksSubject(self.sp)
    self.observer = trackInfoObserver()
    self.subject.register_observer(self.observer)
    self.subject.run()
    time.sleep(10)

  def get_info(self): 
    if self.tracks_info is None:
      self.tracks_info = self.observer.tracks

    track_names = []
    first_item = self.tracks_info

    for item in first_item['items']: # type: ignore
      track_name = item['track']['name']
      track_names.append(track_name)

    return track_names
  
class IdInfo(SongInfo):
  def __init__(self, token_info):
    self.token_info = token_info
    self.sp = spotipy.Spotify(auth=self.token_info['access_token'])
    self.tracks_info = None
    self.subject = TracksSubject(self.sp)
    self.observer = trackInfoObserver()
    self.subject.register_observer(self.observer)
    self.subject.run()
    time.sleep(10)

  def get_info(self): 
    if self.tracks_info is None:
      self.tracks_info = self.observer.tracks

    track_ids = []
    first_item = self.tracks_info

    for item in first_item['items']: # type: ignore
      track_id = item['track']['id']
      track_ids.append(track_id)

    return track_ids

class AlbumInfo(SongInfo):
  def __init__(self, token_info):
    self.token_info = token_info
    self.sp = spotipy.Spotify(auth=self.token_info['access_token'])
    self.tracks_info = None
    self.subject = TracksSubject(self.sp)
    self.observer = trackInfoObserver()
    self.subject.register_observer(self.observer)
    self.subject.run()
    time.sleep(5)

  def get_info(self): 
    if self.tracks_info is None:
       self.tracks_info = self.observer.tracks
 
    image_urls = []
    first_item = self.tracks_info

    for item in first_item['items']: # type: ignore
      image_url = item['track']['album']['images'][0]['url']
      image_urls.append(image_url)

    return image_urls

#Factory Interface
class InfoFactory(ABC):
    @abstractmethod
    def create_artist_info(self, token_info):
        pass

    @abstractmethod
    def create_song_info(self, token_info):
        pass

    @abstractmethod
    def create_album_info(self, token_info):
        pass
    
    @abstractmethod
    def create_id_info(self, token_info):
        pass

# Concerte Factories
class ArtistInfoFactory(InfoFactory):
    def create_artist_info(self, token_info):
        return ArtistInfo(token_info)
    
    def create_song_info(self, token_info):
        return SongInfo(token_info)
    
    def create_album_info(self, token_info):
      return AlbumInfo(token_info)
    
    def create_id_info(self, token_info):
      return IdInfo(token_info)

