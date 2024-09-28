import os
import json
from flask import Flask, session, request, redirect, url_for, render_template
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from flaskr.get_artists import get_artists_blueprint
from flaskr.search_results import search_results_blueprint
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__,  template_folder='templates')
app.config['SECRET_KEY'] = os.urandom(64)
	
app.config['WTF_CSRF_ENABLED'] = False

load_dotenv('/.env')

_client_id = os.getenv("CLIENT_ID")
_client_secret = os.getenv("CLIENT_SECRET")
_redirect_uri = os.getenv("REDIRECT_URI")
_scope = os.getenv("SCOPE")

_cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=_client_id,
    client_secret = _client_secret,
    redirect_uri=_redirect_uri,
    scope=_scope,
    cache_handler=_cache_handler,
    show_dialog=True
)
sp = Spotify(auth_manager=sp_oauth)

search_categories = ['tracks', 'artists']

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

@app.route('/home', methods=["GET", "POST"])
def home():
    # Handle token validation
    if not sp_oauth.validate_token(_cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    # Display user's top 5 artists
    topArtists = sp.current_user_top_artists(limit=50, time_range="medium_term")
    artistInfo = [(pl['name'], pl['uri'][15:], pl['images'][0]['url'], pl['genres']) for pl in topArtists['items']]
    # Find and count genres of the top artists
    genres = []
    for i in artistInfo:
        for j in i[3]:
            genres.append(j)
    print(topArtists)
    count = pd.Series(genres).value_counts()
    print("Element Count")
    print(count)
    # Display user's top 10 tracks
    topTracks = sp.current_user_top_tracks(limit=50)
    trackInfo = [(ti['name'], ti['album']['images'][0]['url']) for ti in topTracks['items']]
    print(artistInfo)
    print(trackInfo)
    return render_template('index.html', indx=artistInfo, tracks=trackInfo, uName= sp.current_user()['display_name'])

@app.route('/search', methods=["GET", "POST"])
def search():
    content = request.form['searched']
    tracks = sp.search(content, type="track", limit=20)
    tracks = tracks['tracks']['items']
    return render_template('search_results.html', results = tracks)

@app.route('/data', methods=["GET"])
def data():
    topArtists = sp.current_user_top_artists(limit=50, time_range="medium_term")
    artistInfo = [(pl['name'], pl['uri'][15:], pl['images'][0]['url'], pl['genres']) for pl in topArtists['items']]
    print(topArtists)
    topTracks = sp.current_user_top_tracks(limit=50)
    trackInfo = [(ti['name'], ti['album']['images'][0]['url']) for ti in topTracks['items']]
    return {
        'Name': sp.current_user()['display_name'], 
        "artists": topArtists['items'],
        "tracks": topTracks['items']
        }
    


app.register_blueprint(get_artists_blueprint)
app.register_blueprint(search_results_blueprint)


if __name__ == '__main__':
    app.run(debug=True)
 