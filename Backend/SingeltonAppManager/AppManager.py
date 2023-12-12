import time
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, url_for, session, redirect #type:ignore
from flask import Flask, request, url_for, session, redirect
from flask import Flask, render_template



app = Flask(__name__,template_folder='../../Frontend/templates', static_folder='../../Frontend/static' )
app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = 'asdkfjhwih4khsgksadhfsakdfjhvn234kjhasfkb3i4h2'
TOKEN_INFO = 'token_info'


class AppManager:
  _instance = None; 
  def __new__(cls):
    if cls._instance is None:
      cls._instance = super(AppManager, cls).__new__(cls)
      cls._instance.initialize()
    return cls._instance
  
  def initialize(self):
    pass
  
  def create_spotify_oauth(self):
      return SpotifyOAuth(
        client_id = "f96ffd1f60e443c5b6b12adeb2863384", 
        client_secret = "101af488cb71478b8093a7d6311ae74d", 
        redirect_uri = url_for('redirect_page', _external=True),
        scope = 'user-library-modify playlist-modify-public playlist-modify-private' # look at the doc to figure out exact scopes 
        ) 
  
  def get_token(self):
    token_info = session.get(TOKEN_INFO, None)
    #if the token does not exist we want to redirect the user
    if not token_info:
      redirect(url_for('login', external=True))
    #if the token is expired get a refresh token
    if(token_info['expires_at'] - int(time.time()) < 60):
      token_info = self.create_spotify_oauth().refresh_access_token(token_info['refresh_token'])
    return token_info
  
