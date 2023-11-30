
from SingeltonAppManager.AppManager import AppManager
from SingeltonAppManager.AppManager import app
from flask import Flask, render_template, request, url_for, session, redirect
import spotipy
from flask import jsonify
from FactoryDisplayLikedSongs.DisplayLikedSongs import SongInfo, ArtistInfo
from SingeltonAppManager.AppManager import TOKEN_INFO # Import the app instance for the token



def main():
  appManager = AppManager()

  @app.route('/' , methods=['GET', 'POST']) #what is below each route is the function that get executed
  def login():
    if request.method == 'POST':
    
      auth_url = appManager.create_spotify_oauth().get_authorize_url()
      return redirect(auth_url) #redirectting them there
      #If the request method is GET, render the login form
    return render_template('login.html')

    
  # once it gets the info from the oath it goes and saves the token inf
  @app.route('/redirect')
  def redirect_page():
    session.clear()
    code = request.args.get('code')
    token_info = appManager.create_spotify_oauth().get_access_token(code) # get_access_token exchanges auth code for a token
    session[TOKEN_INFO] = token_info #stores token info in the session 
    return redirect(url_for('home_page', external = True))


  @app.route('/home_page')
  def home_page():
    return render_template('home.html')


  @app.route('/sort_here_button', methods=['GET', 'POST'], endpoint='sort_here_button')
  def sort_here_button():
    print("Route triggered!")
    return render_template("sortPage.html")
    

  def display_liked():
    try:
      token_info = appManager.get_token()
    except:
      print("User not loged in")
      return redirect('')
    sp = spotipy.Spotify(auth=token_info['access_token'])
    liked_songs = sp.current_user_saved_tracks()
    songs = []
    artists = []
    for track in liked_songs:
      songs.append(track["name"])
    for track in liked_songs:
      artists.append(track["artists"]["name"])

  @app.route('/display_liked', methods=['GET', 'POST'], endpoint='display_liked')
  def display_liked():

    songInfo = SongInfo()
    showLiked = ArtistInfo(songInfo)

    response_data = showLiked.get_info()

    return jsonify(response_data)
    return render_template('sortPage.html', liked_songs = showLiked)
      


  @app.route('/sort_genre', methods=['GET', 'POST'], endpoint='sort_genre')
  def sort_genre():
    try:
      token_info = appManager.get_token()
      sp = spotipy.Spotify(auth=token_info['access_token'])
      #liked_songs = sp.current_user_saved_tracks()
      showLiked = ArtistInfo()
    
    except:
      print("User not loged in")
      return redirect('')
    
    return render_template('sortPage.html', liked_songs = showLiked)
  

  app.run(debug=True)

if __name__ == "__main__":
  main()
  
