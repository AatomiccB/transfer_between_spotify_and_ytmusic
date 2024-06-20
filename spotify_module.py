import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_spotify_client(client_id, client_secret, redirect_uri):
    # Authentication for Spotify
    scope = "user-library-read playlist-read-private"
    return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                     client_secret=client_secret,
                                                     redirect_uri=redirect_uri,
                                                     scope=scope))

def get_liked_songs(sp):
    results = sp.current_user_saved_tracks(limit=50)
    tracks = [item['track']['name'] + ' ' + item['track']['artists'][0]['name'] for item in results['items'] if item['track']]

    while results['next']:
        results = sp.next(results)
        tracks.extend([item['track']['name'] + ' ' + item['track']['artists'][0]['name'] for item in results['items'] if item['track']])

    logger.info(f"Found {len(tracks)} liked songs on Spotify")
    return tracks

def get_spotify_playlists(sp):
    playlists = sp.current_user_playlists()
    playlist_data = []
    for playlist in playlists['items']:
        logger.info(f"Fetching tracks for playlist: {playlist['name']}")
        results = sp.playlist_items(playlist['id'])
        if results and 'items' in results:
            tracks = [item['track']['name'] + ' ' + item['track']['artists'][0]['name'] for item in results['items'] if item['track']]
            playlist_data.append({'name': playlist['name'], 'tracks': tracks})
            logger.info(f"Found {len(tracks)} tracks in playlist: {playlist['name']}")
        else:
            logger.warning(f"No items found in playlist: {playlist['name']}")
    return playlist_data
