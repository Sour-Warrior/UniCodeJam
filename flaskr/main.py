import os
from flask import Flask, session, request, redirect, url_for, render_template
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

app = Flask(__name__,  template_folder='templates')
app.config['SECRET_KEY'] = os.urandom(64)

_client_id = 'bca5251cd35842258f6b4390c653a2e1'
_client_secret = '5466f21024b646b4834519d6b316b7bf'
_redirect_uri = 'http://localhost:5000/callback'
_scope = 'user-top-read'

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
    pInfo = [(pl['name']) for pl in playlists['items']]
    playlists_html = '<br>'.join([f'{name[0]}' for name in pInfo])
    artistInfo = sp.artist('2n2RSaZqBuUUukhbLlpnE6')
    print(artistInfo['name'])
    return render_template('index.html', indx=pInfo )

@app.route('/artistInfo')
def artistInfo():
    if not sp_oauth.validate_token(_cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    artistInfo = sp.artist('2n2RSaZqBuUUukhbLlpnE6')
    print(artistInfo)
    aInfo = artistInfo['name']
    #playlists_html = '<br>'.join([f'{name[0]}' for name in pInfo])
    return render_template('artist.html', artist = aInfo )



if __name__ == '__main__':
    app.run(debug=True)
 