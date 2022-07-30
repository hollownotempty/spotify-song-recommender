from genericpath import isfile
from pathlib import Path
from spotipy.oauth2 import SpotifyOAuth

import spotipy 
import os
if os.path.isfile('env.py'):
    import env # all the spotify credentials stored in an env.py file

def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist', limit=50)
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


def get_recommendations_for_artist(artist):
    track_ids = []
    for i in range(10):
        results = sp.recommendations(seed_artists=[artist['id']])
        for track in results['tracks']:
            track_ids.append("spotify:track:" + track['id'])

    track_number = int(input("How many tracks would you like?\n"))
    new_track_ids = list( dict.fromkeys(track_ids) ) # turn track_ids list into a dictionary and back to remove duplicates
    final_list = new_track_ids[:track_number] 

    return final_list

def create_new_playlist(playlist, track_ids):
    sp.playlist_add_items(playlist, track_ids, position=None)
    print("Playlist successfully created")


def main():
    user_id = sp.me()['id']
    artist_name = input("Please enter an artist:\n")
    artist = get_artist(artist_name)
    if artist:
        playlist_name = str("IIL: " + artist_name.title())
        playlist = sp.user_playlist_create(user_id, playlist_name)
        track_ids = get_recommendations_for_artist(artist)
        create_new_playlist(playlist['id'], track_ids)
    else:
        print("Couldn't find artist, try again?")
        main()
    


if __name__ == '__main__':
    scope = 'playlist-modify-public'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    main()