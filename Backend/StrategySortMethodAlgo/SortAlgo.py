from flask import session, redirect, url_for
from abc import ABC, abstractmethod
from SingeltonAppManager.AppManager import app
import spotipy
from abc import ABC, abstractmethod

class SortingStrategy(ABC):
    @abstractmethod
    def sort(self, tracks,sp):
        pass

class GenreSortingStrategy(SortingStrategy):
    def sort(self,tracks,sp):
        genre_song_dict = {}
        for song in tracks:
            genres = sp.artist(song['track']['artists'][0]['id'])['genres'] # type: ignore
            if genres:
                shortest_genre = [genre.title() for genre in genres if len(genre) == len(min(genres, key=len))][-1]
                if shortest_genre not in genre_song_dict: genre_song_dict[shortest_genre] = []
                genre_song_dict[shortest_genre].append(song['track']['name'])
        return genre_song_dict
    
class ArtistSortingStrategy(SortingStrategy):
    def sort(self,tracks,sp):
        artist_song_dict = {}
        for song in tracks:
            artist_name = song['track']['artists'][0]['name']
            if artist_name not in artist_song_dict: artist_song_dict[artist_name] = []
            artist_song_dict[artist_name].append(song['track']['name'])
        return artist_song_dict
    
class MoodSortingStrategy(SortingStrategy):
    def sort(self,tracks,sp):
        mood_song_dict = {'Happy': [], 'Sad': [], 'Energetic': [], 'Calm': []}
        for song in tracks:
            features = sp.audio_features(song['track']['id'])[0] # type: ignore
            if features:
                valence = features['valence']
                energy = features['energy']
                if valence > 0.5 and energy > 0.5: mood = 'Happy'
                elif valence < 0.5 and energy < 0.5: mood = 'Sad'
                elif energy > 0.5: mood = 'Energetic'
                else: mood = 'Calm'
                mood_song_dict[mood].append(song['track']['name'])
        return mood_song_dict

class SortAlgo():
    def __init__(self, strategy: SortingStrategy, token_info):
        self.strategy = strategy
        self.token_info = token_info

    def sort(self):
        tracks = []
        sp = spotipy.Spotify(auth=self.token_info['access_token'])
        for offset in range(0, 1000, 50):
            response = sp.current_user_saved_tracks(limit = 50, offset=offset)
            if len(response) == 0: break # type: ignore
            tracks.extend(response.get('items', [])) # type: ignore
        return self.strategy.sort(tracks,sp)