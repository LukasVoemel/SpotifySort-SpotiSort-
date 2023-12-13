from abc import ABC, abstractmethod
import spotipy

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
                if shortest_genre not in genre_song_dict: 
                    genre_song_dict[shortest_genre] = {'songs':[], 'song_uri':[]}
                genre_song_dict[shortest_genre]['songs'].append(song['track']['name'])
                genre_song_dict[shortest_genre]['song_uri'].append(song['track']['uri'])
        return genre_song_dict
    
class ArtistSortingStrategy(SortingStrategy):
    def sort(self,tracks,sp):
        artist_song_dict = {}
        for song in tracks:
            artist_name = song['track']['artists'][0]['name']
            if artist_name not in artist_song_dict: 
                artist_song_dict[artist_name] = {'songs':[], 'song_uri':[]}
            artist_song_dict[artist_name]['songs'].append(song['track']['name'])
            artist_song_dict[artist_name]['song_uri'].append(song['track']['uri'])
        return artist_song_dict
    
class MoodSortingStrategy(SortingStrategy):
    def sort(self,tracks,sp):
        mood_song_dict = {'Happy': {'songs':[], 'song_uri':[]}, 'Sad': {'songs':[], 'song_uri':[]}, 'Energetic': {'songs':[], 'song_uri':[]}, 'Calm': {'songs':[], 'song_uri':[]}}
        for song in tracks:
            features = sp.audio_features(song['track']['id'])[0] # type: ignore
            if features:
                valence = features['valence']
                energy = features['energy']
                if valence > 0.5 and energy > 0.5: mood = 'Happy'
                elif valence < 0.5 and energy < 0.5: mood = 'Sad'
                elif energy > 0.5: mood = 'Energetic'
                else: mood = 'Calm'
                mood_song_dict[mood]['songs'].append(song['track']['name'])
                mood_song_dict[mood]['song_uri'].append(song['track']['uri'])
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