from flask import session, redirect, url_for
from abc import ABC, abstractmethod
from SingeltonAppManager.AppManager import app
import spotipy

class SortAlgo():
    
    def __init__(self, token_info):
        self.token_info = token_info

    def sort_genreAlgo(self):
        sp = spotipy.Spotify(auth=self.token_info['access_token'])
        tracks = []
        genre_song_dict = {}
        for offset in range(0, 1000, 50):
            response = spotipy.Spotify(auth=self.token_info['access_token']).current_user_saved_tracks(limit = 50, offset=offset)
            if len(response) == 0: break # type: ignore
            tracks.extend(response.get('items', [])) # type: ignore
        for song in tracks:
            genres = sp.artist(song['track']['artists'][0]['id'])['genres'] # type: ignore
            if genres:
                shortest_genre = [genre.title() for genre in genres if len(genre) == len(min(genres, key=len))][-1]
                if shortest_genre not in genre_song_dict: genre_song_dict[shortest_genre] = []
                genre_song_dict[shortest_genre].append(song['track']['name'])
        return genre_song_dict
    
    def sort_artistAlgo(self):
        tracks = []
        artist_song_dict = {}
        for offset in range(0, 1000, 50):
            response = spotipy.Spotify(auth=self.token_info['access_token']).current_user_saved_tracks(limit=50, offset=offset)
            if len(response) == 0: break # type: ignore
            tracks.extend(response.get('items', []))  # type: ignore
        for song in tracks:
            artist_name = song['track']['artists'][0]['name']
            if artist_name not in artist_song_dict: artist_song_dict[artist_name] = []
            artist_song_dict[artist_name].append(song['track']['name'])
        return artist_song_dict

    def sort_moodAlgo(self):
        sp = spotipy.Spotify(auth=self.token_info['access_token'])
        tracks = []
        mood_song_dict = {'Happy': [], 'Sad': [], 'Energetic': [], 'Calm': []}
        for offset in range(0, 1000, 50):
            response = spotipy.Spotify(auth=self.token_info['access_token']).current_user_saved_tracks(limit=50, offset=offset)
            if len(response) == 0: break # type: ignore
            tracks.extend(response.get('items', []))  # type: ignore
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
