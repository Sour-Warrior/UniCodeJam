from flask import Blueprint, Flask, session, request, redirect, url_for
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler


get_playlists = Blueprint(name='get_playlists',import_name=__name__)
