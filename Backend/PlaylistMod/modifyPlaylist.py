from SingeltonAppManager.AppManager import AppManager
from SingeltonAppManager.AppManager import TOKEN_INFO # Import the app instance for the token
import spotipy

class PlayMod():
    def __init__(self,token_info):
        self.token_info = token_info
        self.sp = spotipy.Spotify(auth=self.token_info['access_token'])

    def remove_song(self,song_id):
        # sp = spotipy.Spotify(auth=self.token_info['access_token'])
        # sp.current_user_saved_tracks_delete(tracks=[song_id])
        # return redirect(url_for('sort_here_button'))
        return self.token_info

    def create_playlist(self, name, song_list):
        user_id = self.sp.current_user()['id']
        playlist = self.sp.user_playlist_create(user_id, name, public=False)

        # Splitting the song_uris list into chunks of 100, as Spotify has a limit
        # on the number of tracks that can be added at once.
        for i in range (len(song_list)):
            self.sp.playlist_add_items(playlist['id'], song_list[i])
