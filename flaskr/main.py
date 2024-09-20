import os
from flask import Flask, session, request, redirect, url_for, render_template
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from get_artists import get_artists_blueprint
from dotenv import load_dotenv
from pathlib import Path

app = Flask(__name__,  template_folder='templates')
app.config['SECRET_KEY'] = os.urandom(64)

load_dotenv()

_client_id = os.getenv("CLIENT_ID")
_client_secret = os.getenv("CLIENT_SECRET")
_redirect_uri = os.getenv("REDIRECT_URI")
_scope = os.getenv("SCOPE")

_cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=_client_id,
    client_secret=_client_secret,
    redirect_uri=_redirect_uri,
    scope=_scope,
    cache_handler=_cache_handler,
    show_dialog=True
)
sp = Spotify(auth_manager=sp_oauth)

@app.route('/')
def login():
    if not sp_oauth.validate_token(_cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('home'))



@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('home'))

@app.route('/home')
def home():
    if not sp_oauth.validate_token(_cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    playlists = sp.current_user_top_artists(limit=5)
    print(playlists)
    pInfo = [(pl['name'], pl['uri'][15:], pl['images'][0]['url']) for pl in playlists['items']]
    print(sp.current_user())
    return render_template('index.html', indx=pInfo, uName= sp.current_user()['display_name'])


app.register_blueprint(get_artists_blueprint)


if __name__ == '__main__':
    app.run(debug=True)
 