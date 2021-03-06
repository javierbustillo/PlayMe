import json
import random

import requests

from SpotifyAPI import SpotifyAPI
import csv


def get_urls(track_ids):
    print('Preparing urls...')

    url = '/audio-features/?ids='
    urls = []
    count = 0
    current_url = url

    while track_ids:
        track_id = track_ids.pop()
        if track_id is None:
            continue
        current_url += track_id + ','
        count += 1
        if count % 100 == 0:
            urls.append(current_url[:-1])
            current_url = url

    urls.append(current_url[:-1])
    return urls


def get_audio_features(urls):
    print("Getting audio features...")
    features = []
    for url in urls:
        track_features = SpotifyAPI().request_data(url)
        if track_features is None:
            continue
        audio_features = track_features['audio_features']
        for audio_feature in audio_features:
            if audio_feature is None:
                continue
            features.append(audio_feature)
    return features


def scrape(search_term):
    searched_playlists = SpotifyAPI().search_playlists(search_term)
    playlists_tracks_id = []
    playlist_tracks = []
    track_ids = []

    for playlist in searched_playlists:
        playlists_tracks_id.append(playlist["id"])

    print("Getting tracks from playlists...")
    for playlist_id in playlists_tracks_id:
        playlist_tracks.append(SpotifyAPI().get_playlist_tracks(playlist_id))

    for playlist_track in playlist_tracks:
        for track in playlist_track:
            if track['track'] is None:
                continue
            track_ids.append(track['track']['id'])

    urls = get_urls(track_ids)
    features = get_audio_features(urls)

    print("Creating dataset...")
    with open('audio_feat.csv', mode='a', newline='') as features_file:
        feature_writer = csv.writer(features_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        header = ["danceability", "energy", "term"]
        feature_list = []
        for feature in features:
            feature_list.append([feature['danceability'], feature['energy'], feature['acousticness'],
                                 feature['instrumentalness'], feature['liveness'],
                                 feature['speechiness'], feature['valence'], feature['tempo'],  search_term])
        feature_writer.writerows(feature_list)


def generate_rand_data():
    with open('audio_feat.csv', mode='a') as features_file:
        feature_writer = csv.writer(features_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        header = ["danceability", "energy", "term"]
        feature_list = []
        for feature in range(1000):
            feature_list.append([random.random(), random.random(), random.random(),
                                 random.random(), random.random(), random.random(),
                                 random.random(), random.random(), random.uniform(60, 120), "random"])
        feature_writer.writerows(feature_list)

