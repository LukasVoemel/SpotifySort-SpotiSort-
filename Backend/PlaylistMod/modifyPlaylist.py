from SingeltonAppManager.AppManager import AppManager
from SingeltonAppManager.AppManager import app
from flask import render_template, request, url_for, session, redirect, jsonify #type:ignore
from SingeltonAppManager.AppManager import TOKEN_INFO # Import the app instance for the token
import spotipy

class PlayMod():
    def __init__(self,token_info):
        self.token_info = token_info

    def remove_song(self,song_id):
        # sp = spotipy.Spotify(auth=self.token_info['access_token'])
        # sp.current_user_saved_tracks_delete(tracks=[song_id])
        # return redirect(url_for('sort_here_button'))
        return self.token_info

    def create_playlist(self, name, song_list):
        sp = spotipy.Spotify(auth=self.token_info['access_token'])

        user_id = sp.current_user()['id']
        playlist = sp.user_playlist_create(user_id, name, public=False)
        
        sp.playlist_add_items(playlist_id=playlist['id'], items=song_list)
        print("Playlist " + playlist['name'] + 'created')
