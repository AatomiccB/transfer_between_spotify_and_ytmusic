import logging
from spotify_module import get_liked_songs, get_spotify_playlists
from ytmusic_module import create_ytmusic_playlists, create_liked_songs_playlist


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':

    # Fetch playlists and liked songs from Spotify
    spotify_playlists = get_spotify_playlists()
    liked_songs = get_liked_songs()

    # Create YouTube Music playlists and add liked songs
    create_ytmusic_playlists(spotify_playlists)
    create_liked_songs_playlist(liked_songs)








 