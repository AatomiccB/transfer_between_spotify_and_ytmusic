from ytmusicapi import YTMusic
import logging
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def playlist_exists(ytmusic_instance, name):
    playlists = ytmusic_instance.get_library_playlists()
    for playlist in playlists:
        if playlist['title'].lower() == name.lower():
            return playlist['playlistId']
    return None


def create_ytmusic_playlists(ytmusic_instance, spotify_playlists):
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
                            logger.warning(
                                f"Conflict error when adding track '{track}' to playlist '{playlist['name']}': {e}")
                        else:
                            logger.error(f"Error adding track '{track}' to playlist '{playlist['name']}': {e}")
                else:
                    # logger.info(f"Track '{track}' already exists in playlist '{playlist['name']}'")
                    existing_tracks += 1
                    # print(existing_tracks)
                    # print(existing_tracks)
            else:
                logger.info(f"Track '{track}' not found on YouTube Music.")

        # Display total number of tracks in the Spotify playlist and the number of tracks added and existing in the YouTube Music playlist
        # logger.info(f"Total tracks in Spotify playlist '{playlist['name']}': {len(playlist['tracks'])}")
        logger.info(f"Tracks added to playlist '{playlist['name']}': {added_tracks}")
        logger.info(f"Existing tracks in playlist '{playlist['name']}': {existing_tracks}")


def create_liked_songs_playlist(ytmusic_instance, liked_songs):
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
                # logger.info(f"Track '{track}' already exists in playlist '{playlist_name}'")
                existing_tracks += 1
                # print("Existing track count: ",existing_tracks)
        else:
            logger.info(f"Track '{track}' not found on YouTube Music.")

    # Display summary for the playlist
    logger.info(f"Playlist '{playlist_name}' summary:")
    logger.info(f"Total liked songs: {len(liked_songs)}")
    logger.info(f"Total tracks added: {added_tracks}")
    logger.info(f"Total existing tracks: {existing_tracks}")
