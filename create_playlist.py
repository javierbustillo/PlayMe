import json
from random import shuffle

import requests

from SpotifyAPI import SpotifyAPI
from joblib import load

from script import get_urls, get_audio_features


def get_liked_songs():
    liked_songs = SpotifyAPI().get_liked_songs()['items']
    offset = 0
    saved_liked_songs = []
    while liked_songs:
        offset += 50
        for liked_song in liked_songs:
            saved_liked_songs.append(liked_song)
        liked_songs = SpotifyAPI().get_liked_songs(offset=offset)['items']
    return saved_liked_songs


def get_top_songs():
    track_ids =[]
    liked_songs = SpotifyAPI().get_liked_songs()
    next = liked_songs['next']
    while next != 'null':
        for track in liked_songs['items']:
            track_id = track['track']['id']
            track_ids.append(track_id)
        header = {'Authorization': 'Bearer ' + SpotifyAPI.tok}
        if next is None:
            break
        response = requests.get(next, headers=header)
        liked_songs = json.loads(response.text)
        next = liked_songs['next']
    return track_ids


def create_playlist(search_term):
    recommender = load('recommender.joblib')
    liked_songs = get_liked_songs()
    track_ids = []
    tracks_for_playlist = []

    for liked_song in liked_songs:
        track_ids.append(liked_song['track']['id'])

    urls = get_urls(track_ids)
    features = get_audio_features(urls)
    shuffle(features)

    feature_list = []
    for feature in features:
        feature_list.append([feature['danceability'], feature['energy'], feature['acousticness'],
                             feature['instrumentalness'], feature['liveness'],
                             feature['speechiness'], feature['valence'], feature['tempo']])

    print("Analyzing liked songs...")
    for index, feature in enumerate(feature_list):
        if recommender.predict([feature]) == search_term:
            tracks_for_playlist.append(index)

    print(f"Amount of matches: {len(tracks_for_playlist)} / {len(feature_list)}")

    playlist_id = SpotifyAPI().create_playlist(SpotifyAPI().get_user_info()['id'], search_term)
    tracks_to_add = []
    for count, index in enumerate(tracks_for_playlist):
        if count == 100:
            break
        track = features[index]
        tracks_to_add.append(track['id'])

    print("Adding tracks to playlists...")
    SpotifyAPI().add_tracks_to_playlist(playlist_id, tracks_to_add)
