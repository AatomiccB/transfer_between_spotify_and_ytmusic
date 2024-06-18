import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Authentication for YouTube Music
#ytmusic = YTMusic('headers_auth.json')
# Spotify API credentials
Spotipy_client_id = 'your_Spotipy_client_id'
Spotipy_client_secret = 'your_Spotipy_client_secret'
spotipy_redirect_uri = 'your_spotipy_redirect_uri'

# Authentication for Spotify
scope = "user-library-read playlist-read-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=Spotipy_client_id,
                                               client_secret=Spotipy_client_secret,
                                               redirect_uri=spotipy_redirect_uri,
                                               scope=scope))


def get_spotify_playlists():
    playlists = sp.current_user_playlists()
    playlist_data = []
    for playlist in playlists['items']:
        logger.info(f"Fetching tracks for playlist: {playlist['name']}")
        results = sp.playlist_items(playlist['id'])
        if results and 'items' in results:
            tracks = [item['track']['name'] + ' ' + item['track']['artists'][0]['name'] for item in results['items'] if
                      item['track']]
            playlist_data.append({'name': playlist['name'], 'tracks': tracks})
            logger.info(f"Found {len(tracks)} tracks in playlist: {playlist['name']}")
        else:
            logger.warning(f"No items found in playlist: {playlist['name']}")
    return playlist_data


def create_playlist(self, name, info, privacy="PRIVATE", tracks=None):
    return music_instance.create_playlist(name, info, privacy, video_ids=tracks)


music_instance = YTMusic('browser.json')


def create_music_playlists(spotify_playlists):
    for playlist in spotify_playlists:

        try:
            playlist_id = music_instance.create_playlist(playlist['name'], 'Playlist imported from Spotify')
            for track in playlist['tracks']:
                search_results = music_instance.search(track, filter='songs')
                if search_results:
                    song_id = search_results[0]['videoId']
                    music_instance.add_playlist_items(playlist_id, [song_id])
        except Exception as e:
            print(f"Error creating playlist: {e}")



if __name__ == '__main__':
    spotify_playlists = get_spotify_playlists()
    create_music_playlists(spotify_playlists)
