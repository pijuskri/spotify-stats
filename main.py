from dotenv import load_dotenv
import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import itertools

load_dotenv()
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="7c968afe5eef48fdb0c909c898304f7c",
                                                           client_secret=CLIENT_SECRET))
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def show_tracks(results):
    for i, item in enumerate(results['items']):
        track = item['track']
        print(f"   {i} {track['artists'][0]['name']:>32.32} {track['name']}")


if __name__ == '__main__':
    scope = 'playlist-read-private'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="7c968afe5eef48fdb0c909c898304f7c",
                                                           client_secret=CLIENT_SECRET,
                                                   redirect_uri='http://127.0.0.1:3000', scope=scope))

    playlists = sp.current_user_playlists()
    user_id = sp.me()['id']
    dfs = []
    for playlist in playlists['items']:
        if playlist['owner']['id'] == user_id and playlist['name']:
            print()
            print(playlist['name'])
            print('  total tracks', playlist['tracks']['total'])

            authors = []
            tracks = sp.playlist_items(playlist['id'], fields="items,next", additional_types=('tracks', ))
            #show_tracks(tracks)

            while tracks['next']:
                tracks = sp.next(tracks)
                author_iter = [track['track']['artists'][0]['name'] for track in tracks['items']]
                authors.extend(author_iter)
                #show_tracks(tracks)
            df = pd.DataFrame(authors, columns =['Artist'])
            df['playlist'] = playlist['name']
            dfs.append(df)
    pd.concat(dfs, ignore_index=True).to_csv('dater.csv', index=False)