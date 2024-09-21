import os
from flask import Flask, session, request, redirect, url_for, render_template, Blueprint
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from dotenv import load_dotenv
from pathlib import Path

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

search_results_blueprint = Blueprint('search_results', __name__, template_folder='templates')
@search_results_blueprint.route('/searchResults/<content>')
def get_results(content):
    if not sp_oauth.validate_token(_cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    results = sp.search(content,type='track')
    print(results)
    return render_template('search_results.html')