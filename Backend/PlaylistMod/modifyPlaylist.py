from SingeltonAppManager.AppManager import AppManager
from SingeltonAppManager.AppManager import app
from flask import render_template, request, url_for, session, redirect, jsonify #type:ignore
from SingeltonAppManager.AppManager import TOKEN_INFO # Import the app instance for the token

class PlayMod():
    def __init__(self,token_info):
        self.token_info = token_info

    def remove_song(self,song_id):
        # sp = spotipy.Spotify(auth=token_info['access_token'])
        # sp.current_user_saved_tracks_delete(tracks=[song_id])
        # return redirect(url_for('sort_here_button'))
        return self.token_info
        
