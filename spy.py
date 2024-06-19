import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Authentication for YouTube Music
ytmusic_instance = YTMusic('browser.json')

# Function to check if a playlist exists in YouTube Music
def playlist_exists(ytmusic_instance, name):
    playlists = ytmusic_instance.get_library_playlists()
    for playlist in playlists:
        if playlist['title'].lower() == name.lower():
            return playlist['playlistId']
    return None

# Function to get liked songs from Spotify
def get_liked_songs():
    results = sp.current_user_saved_tracks(limit=50)
    tracks = [item['track']['name'] + ' ' + item['track']['artists'][0]['name'] for item in results['items'] if item['track']]

    while results['next']:
        results = sp.next(results)
        tracks.extend([item['track']['name'] + ' ' + item['track']['artists'][0]['name'] for item in results['items'] if item['track']])

    logger.info(f"Found {len(tracks)} liked songs on Spotify")
    return tracks

# Function to create YouTube Music playlists and add songs
def create_ytmusic_playlists(spotify_playlists):
    for playlist in spotify_playlists:
        print("----------------")
        playlist_id = playlist_exists(ytmusic_instance, playlist['name'])
        if playlist_id:
            logger.info(f"Playlist '{playlist['name']}' already exists. Adding missing songs.")
        else:
            playlist_id = ytmusic_instance.create_playlist(playlist['name'], 'Playlist imported from Spotify')
            logger.info(f"Created new playlist '{playlist['name']}'.")

        # Get current tracks in the playlist
        current_tracks = ytmusic_instance.get_playlist(playlist_id)['tracks']
        current_track_ids = set([track['videoId'] for track in current_tracks])

        logger.info(f"Total tracks in Spotify playlist '{playlist['name']}': {len(playlist['tracks'])}")
        # Add only new tracks
        added_tracks = 0
        existing_tracks = 0
        for track in playlist['tracks']:
            search_results = ytmusic_instance.search(track, filter='songs')
            if search_results:
                song_id = search_results[0]['videoId']
                if song_id not in current_track_ids:
                    try:
                        ytmusic_instance.add_playlist_items(playlist_id, [song_id])
                        logger.info(f"Added track '{track}' to playlist '{playlist['name']}'")
                        added_tracks += 1
                    except Exception as e:
                        if 'HTTP 409' in str(e):
                            logger.warning(f"Conflict error when adding track '{track}' to playlist '{playlist['name']}': {e}")
                        else:
                            logger.error(f"Error adding track '{track}' to playlist '{playlist['name']}': {e}")
                else:
                    #logger.info(f"Track '{track}' already exists in playlist '{playlist['name']}'")
                    existing_tracks += 1
            else:
                logger.info(f"Track '{track}' not found on YouTube Music.")

        # Display total number of tracks in the Spotify playlist and the number of tracks added and existing in the YouTube Music playlist
        #logger.info(f"Total tracks in Spotify playlist '{playlist['name']}': {len(playlist['tracks'])}")
        logger.info(f"Tracks added to playlist '{playlist['name']}': {added_tracks}")
        logger.info(f"Existing tracks in playlist '{playlist['name']}': {existing_tracks}")


# Function to get Spotify playlists
def get_spotify_playlists():
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

# Function to create a new YouTube Music playlist for liked songs from Spotify
def create_liked_songs_playlist(liked_songs):
    playlist_name = "Liked from Spotify"
    playlist_id = playlist_exists(ytmusic_instance, playlist_name)

    if playlist_id:
        logger.info(f"Playlist '{playlist_name}' already exists. Adding missing songs.")
    else:
        playlist_id = ytmusic_instance.create_playlist(playlist_name, 'Liked songs imported from Spotify')
        logger.info(f"Created new playlist '{playlist_name}'.")

    # Get current tracks in the playlist
    current_tracks = ytmusic_instance.get_playlist(playlist_id)['tracks']
    current_track_ids = set([track['videoId'] for track in current_tracks])

    # Add only new tracks
    added_tracks = 0
    existing_tracks = 0
    for track in liked_songs:
        search_results = ytmusic_instance.search(track, filter='songs')
        if search_results:
            song_id = search_results[0]['videoId']
            if song_id not in current_track_ids:
                try:
                    ytmusic_instance.add_playlist_items(playlist_id, [song_id])
                    logger.info(f"Added track '{track}' to playlist '{playlist_name}'")
                    added_tracks += 1
                except Exception as e:
                    if 'HTTP 409' in str(e):
                        logger.warning(f"Conflict error when adding track '{track}' to playlist '{playlist_name}': {e}")
                    else:
                        logger.error(f"Error adding track '{track}' to playlist '{playlist_name}': {e}")
            else:
                #logger.info(f"Track '{track}' already exists in playlist '{playlist_name}'")
                existing_tracks += 1
                #print("Existing track count: ",existing_tracks)
        else:
            logger.info(f"Track '{track}' not found on YouTube Music.")

    # Display summary for the playlist
    logger.info(f"Playlist '{playlist_name}' summary:")
    logger.info(f"Total liked songs: {len(liked_songs)}")
    logger.info(f"Total tracks added: {added_tracks}")
    logger.info(f"Total existing tracks: {existing_tracks}")



if __name__ == '__main__':
    # Fetch playlists and liked songs from Spotify
    spotify_playlists = get_spotify_playlists()
    liked_songs = get_liked_songs()

    # Create YouTube Music playlists and add liked songs
    create_ytmusic_playlists(spotify_playlists)
    create_liked_songs_playlist(liked_songs)
