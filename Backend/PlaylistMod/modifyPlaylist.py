import spotipy

class PlayMod():
    def __init__(self,token_info):
        self.token_info = token_info
        self.sp = spotipy.Spotify(auth=self.token_info['access_token'])

    def remove_song(self,song_id,liked_songs):
        self.sp.current_user_saved_tracks_delete([song_id])
        for item in liked_songs:
            if(item[3] == song_id): liked_songs.remove(item)
        return liked_songs
<<<<<<< HEAD
        
=======
>>>>>>> 90508bfd294098a0794cef7e7dc8b948b85087a8

    def create_playlist(self, name, song_list):
        user_id = self.sp.current_user()['id'] #type:ignore
        self.sp.user_playlist_add_tracks(user_id, self.sp.user_playlist_create(user_id, name, public=False)['id'],eval(song_list)) #type:ignore
