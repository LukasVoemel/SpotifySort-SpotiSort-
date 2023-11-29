
import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template, request, url_for, session, redirect
from SingletonPattern_API.SpotifyAuthManager import SpotifyAuthManager

app = Flask(__name__,template_folder='../Frontend/templates', static_folder='../Frontend/static' )
app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = 'asdkfjhwih4khsgksadhfsakdfjhvn234kjhasfkb3i4h2'
TOKEN_INFO = 'token_info'

#Since this seems to be a much easier project we can sort by very specific things, so that can be one of the classes
@app.route('/' , methods=['GET', 'POST']) #what is below each route is the function that get executed
# def login():
#   auth_url = create_spotify_oauth().get_authorize_url()
#   return redirect(auth_url) #redirectting them there

def login():
  if request.method == 'POST':
    auth_url = SpotifyAuthManager().spotify_oauth.get_authorize_url()
    return redirect(auth_url) #redirectting them there
    #If the request method is GET, render the login form
  return render_template('login.html')

# once it gets the info from the oath it goes and saves the token inf
@app.route('/redirect')
def redirect_page():
  session.clear()
  code = request.args.get('code')
  token_info = SpotifyAuthManager().spotify_oauth.get_access_token(code)
  session[TOKEN_INFO] = token_info #stores token info in the session 
  return redirect(url_for('home_page', external = True))

@app.route('/home_page')
def home_page():
  return render_template('home.html')


@app.route('/likedSongs')
def liked_songs():
  try:
    token_info = get_token()
  except:
    print("User not loged in")
    return redirect('')
  sp = spotipy.Spotify(auth=token_info['access_token'])
  liked_songs = sp.current_user_saved_tracks()
  return liked_songs

def get_token():
  token_info = session.get(TOKEN_INFO, None)
  #if the token does not exist we want to redirect the user
  if not token_info:
    redirect(url_for('login', external=True))
  now = int(time.time())
  is_expired = token_info['expires_at'] - now < 60

  #if the token is expired get a refresh token
  if is_expired:
        spotify_oauth = SpotifyAuthManager().spotify_oauth
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])
  
  return token_info


app.run(debug=True)