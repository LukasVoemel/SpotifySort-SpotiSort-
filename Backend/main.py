from PlaylistMod.modifyPlaylist import PlayMod
from SingeltonAppManager.AppManager import AppManager
from SingeltonAppManager.AppManager import app
from flask import render_template, request, url_for, session, redirect, jsonify #type:ignore
from FactoryDisplayLikedSongs.DisplayLikedSongs import ArtistInfoFactory
from SingeltonAppManager.AppManager import TOKEN_INFO # Import the app instance for the token
from StrategySortMethodAlgo.SortAlgo import MoodSortingStrategy, ArtistSortingStrategy, GenreSortingStrategy, SortAlgo

def main():
  appManager = AppManager()
  
  @app.route('/' , methods=['GET', 'POST']) #what is below each route is the function that get executed
  def login():
    if request.method == 'POST':
      return redirect(appManager.create_spotify_oauth().get_authorize_url()) #redirectting them there
      #If the request method is GET, render the login form
    return render_template('login.html')

  # once it gets the info from the oath it goes and saves the token inf
  @app.route('/redirect')
  def redirect_page():
    session.clear()
    token_info = appManager.create_spotify_oauth().get_access_token(request.args.get('code')) # get_access_token exchanges auth code for a token
    session[TOKEN_INFO] = token_info #stores token info in the session 
    return redirect(url_for('home_page', external = True))
   
  @app.route('/home_page')
  def home_page():
    return render_template('home.html')

  @app.route('/sort_here_button', methods=['GET', 'POST'], endpoint='sort_here_button')
  def sort_here_button():
    #this is where the facotory gets the data from
    factory = ArtistInfoFactory()
    artist_name_out = factory.create_artist_info(appManager.get_token()).get_info()
    song_name_out = factory.create_song_info(appManager.get_token()).get_info()
    album_picture_out = factory.create_album_info(appManager.get_token()).get_info()
<<<<<<< HEAD

    id_out = factory.create_id_info(appManager.get_token()).get_info()
    #zips up all the varibles to send to the html 
    artist_and_song_name = list(zip(artist_name_out, song_name_out, album_picture_out, id_out))

=======
    id_out = factory.create_id_info(appManager.get_token()).get_info()
    #zips up all the varibles to send to the html 
    artist_and_song_name = list(zip(artist_name_out, song_name_out, album_picture_out, id_out))
>>>>>>> b6b1ae3eb14494cd3faeeccee2389e11e5e441c7
    return render_template('sortPage.html', artist_and_song_name=artist_and_song_name)
  
  @app.route('/sort_genre', methods=['GET', 'POST'], endpoint='sort_genre')
  def sort_genre():
    return render_template('playlistCreate.html', playlist=SortAlgo(GenreSortingStrategy(), appManager.get_token()).sort())
  
  @app.route('/sort_artist', methods=['GET', 'POST'], endpoint='sort_artist')
  def sort_artist():
    return render_template('playlistCreate.html', playlist=SortAlgo(ArtistSortingStrategy(), appManager.get_token()).sort())
  
  @app.route('/sort_mood', methods=['GET', 'POST'], endpoint='sort_mood')
  def sort_mood():
    return render_template('playlistCreate.html', playlist=SortAlgo(MoodSortingStrategy(), appManager.get_token()).sort())
  
  @app.route('/remove_song', methods=['GET','POST'], endpoint='remove_song')
  def remove_song():
      liked_songs = PlayMod(appManager.get_token()).remove_song(request.form['song_id'],eval(request.form['liked_songs']))
      return render_template('sortPage.html', artist_and_song_name=liked_songs)
  
  @app.route('/create_playlist', methods=['GET','POST'], endpoint='create_playlist')
  def create_playlist():
      PlayMod(appManager.get_token()).create_playlist(request.form['playlist_name'],request.form['song_list'])
      return render_template('playlistCreate.html', playlist=eval(request.form['playlist']))

  app.run(debug=True)

if __name__ == "__main__":
  main()
