from genericpath import isfile
from pathlib import Path
from spotipy.oauth2 import SpotifyClientCredentials

import argparse
import logging

import spotipy 
import os
if os.path.isfile('env.py'):
    import env # all the spotify credentials stored in an env.py file


def get_args():
    parser = argparse.ArgumentParser(description='Recommendations for the '
                                     'given artist')
    parser.add_argument('-a', '--artist', required=True, help='Name of Artist')
    return parser.parse_args()


def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


def show_recommendations_for_artist(artist):
    results = sp.recommendations(seed_artists=[artist['id']])
    track = results['tracks'][0]
    logger.info("You're gonna love '" + track['name'] + "' by " + track['artists'][0]['name'] + " - " + track['external_urls']['spotify'])


def main():
    args = get_args()
    artist = get_artist(args.artist)
    if artist:
        show_recommendations_for_artist(artist)
    else:
        logger.error("Can't find that artist", args.artist)


if __name__ == '__main__':
    logger = logging.getLogger('examples.artist_recommendations')
    logging.basicConfig(level='INFO')

    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    main()