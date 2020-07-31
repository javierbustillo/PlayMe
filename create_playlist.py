from random import shuffle

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


def create_playlist(search_term):
    recommender = load('recommender.joblib')
    liked_songs = get_liked_songs()
    track_ids = []
    features = []
    tracks_for_playlist = []

    for liked_song in liked_songs:
        track_ids.append(liked_song['track']['id'])

    urls = get_urls(track_ids)
    features = get_audio_features(urls)
    shuffle(features)

    feature_list = []
    for feature in features:
        feature_list.append([feature['danceability'], feature['energy'], feature['acousticness'],
                             feature['instrumentalness'], feature['liveness'], feature['loudness'],
                             feature['speechiness'], feature['valence'], feature['tempo']])

    for index, feature in enumerate(feature_list):
        if recommender.predict([feature]) == search_term:
            tracks_for_playlist.append(index)

    playlist_id = SpotifyAPI().create_playlist(SpotifyAPI().get_user_info()['id'], search_term)

    for count, index in enumerate(tracks_for_playlist):
        if count == 30:
            break
        track = features[index]
        SpotifyAPI().add_tracks_to_playlist(playlist_id, track['id'])
