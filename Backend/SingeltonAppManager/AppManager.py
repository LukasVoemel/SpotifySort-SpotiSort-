import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template, request, url_for, session, redirect

app = Flask(__name__,template_folder='../../Frontend/templates', static_folder='../../Frontend/static' )

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = 'asdkfjhwih4khsgksadhfsakdfjhvn234kjhasfkb3i4h2'
TOKEN_INFO = 'token_info'



@app.route('/' , methods=['GET', 'POST']) #what is below each route is the function that get executed
def login():
  if request.method == 'POST':
   
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url) #redirectting them there
    #If the request method is GET, render the login form
  return render_template('login.html')

  
# once it gets the info from the oath it goes and saves the token inf
@app.route('/redirect')
def redirect_page():
  session.clear()
  code = request.args.get('code')
  token_info = create_spotify_oauth().get_access_token(code) # get_access_token exchanges auth code for a token
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
    token_info = get_token()
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
    

@app.route('/sort_genre', methods=['GET', 'POST'], endpoint='sort_genre')
def sort_genre():
  #genre sort
  try:
    token_info = get_token()
  except:
    print("User not loged in")
    return redirect('')
  sp = spotipy.Spotify(auth=token_info['access_token'])
  liked_songs = sp.current_user_saved_tracks()
  print((liked_songs))
  return liked_songs
  
# def sort_artist():
#   #artist sort
  
# def sort_mood():
#   #mood sort











def get_token():
  token_info = session.get(TOKEN_INFO, None)
  #if the token does not exist we want to redirect the user
  if not token_info:
    redirect(url_for('login', external=True))
  now = int(time.time())
  is_expired = token_info['expires_at'] - now < 60
  #if the token is expired get a refresh token
  if(is_expired):
    spotify_oauth = create_spotify_oauth()
    token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])

  return token_info

def create_spotify_oauth():
  return SpotifyOAuth(
    client_id = "f96ffd1f60e443c5b6b12adeb2863384", 
    client_secret = "101af488cb71478b8093a7d6311ae74d", 
    redirect_uri = url_for('redirect_page', _external=True),
    scope = 'user-library-read playlist-modify-public playlist-modify-private' # look at the doc to figure out exact scopes 
    ) 
app.run(debug=True)