from genericpath import isfile
from pathlib import Path
from spotipy.oauth2 import SpotifyOAuth

import argparse

import spotipy 
import os
if os.path.isfile('env.py'):
    import env # all the spotify credentials stored in an env.py file


def get_args():
    parser = argparse.ArgumentParser(description='Creates a playlist for user')
    parser.add_argument('-p', '--playlist', required=True,
                        help='Name of Playlist')
    parser.add_argument('-d', '--description', required=False, default='',
                        help='Description of Playlist')
    return parser.parse_args()


def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist', limit=50)
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


def get_recommendations_for_artist(artist):
    results = sp.recommendations(seed_artists=[artist['id']])
    track_ids = []
    for track in results['tracks']:
        track_ids.append("spotify:track:" + track['id'])

    return track_ids

def create_new_playlist(playlist, track_ids):
    sp.playlist_add_items(playlist, track_ids, position=None)
    print("Playlist successfully created")


def main():
    args = get_args()
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user_id, args.playlist)
    artist_name = input("Please enter an artist:\n")
    artist = get_artist(artist_name)
    if artist:
        track_ids = get_recommendations_for_artist(artist)
        create_new_playlist(playlist['id'], track_ids)
    else:
        logger.error("Can't find that artist", args.artist)
    


if __name__ == '__main__':
    scope = 'playlist-modify-public'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    main()