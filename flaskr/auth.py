from flask import Blueprint, Flask, session, request, redirect, url_for
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

auth = Blueprint(name='auth',import_name=__name__)

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

