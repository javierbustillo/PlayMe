import requests
import json


# from Entities.artists import Artists
# from Entities.tracks import Tracks

class SpotifyAPI:
    base_url = 'https://api.spotify.com/v1'
    tok = 'BQDXq0vVcCToCDBwHve_ykmLX7iuAiinR-qrdkHFweuemADR6pO2-BUcO2B_ojkN83MaGixnhrcXwn7a6ciF-JzoF78KjHZP7h9g-Rozt1kXlSQ8rI3htGmj1zkIHEu47rzSGmrD2AUpZZi8vr-Xljevxcpd6oa97aGkEuEUQu8vjUARPovbrE0nOi1F-ASc082ECcfgzv3uYGUeW2tjKsfL0xdP3whLXNUsqgxvMGHOeo0L8yqM10-N_RAGjHCeXEiRpzj8xPHxoDfciFk'

    def request_data(self, url, token=tok, method='GET', body=None):
        header = {'Authorization': 'Bearer ' + token} if token else None
        if method == 'GET':
            response = requests.get(self.base_url + url, headers=header)
        else:
            response = requests.post(self.base_url + url, headers=header, json=body)
        return json.loads(response.text) if response.text else None

    def get_user_info(self):
        user_info = self.request_data('/me', token=self.tok)
        return user_info

    # def get_user_top_tracks_artists(self, token, type_of_top=None):
    #     enumerated = enumerate
    #     user_id = self.get_user_info(token)['id']
    #     ranges = ['long_term', 'medium_term', 'short_term']
    #     users_tops = []
    #     types = [type_of_top] if type_of_top is not None else ['artists', 'tracks']
    #     for type_top in types:
    #         for term in ranges:
    #             tops = self.request_data('/me/top/%s?time_range=%s&limit=50' % (type_top, term), token)['items']
    #             for position, top in enumerated(tops):
    #                 spotify_id = top['id']
    #                 if term == 'short_term':
    #                     term_int = 0
    #                 elif term == 'medium_term':
    #                     term_int = 1
    #                 else:
    #                     term_int = 2
    #                 obj = Artists if type_top == 'artists' else Tracks
    #                 top_obj = obj(spotify_id, term_int, position, user_id)
    #                 users_tops.append(top_obj)
    #     return users_tops

    # def get_user_top_tracks(self, token):
    #     return self.get_user_top_tracks_artists(token, 'tracks')
    #
    # def get_user_top_artists(self, token):
    #     return self.get_user_top_tracks_artists(token, 'artists')

    def get_user_by_id(self, token, spotify_id):
        return self.request_data('/users/%s' % spotify_id, token=token)

    def get_track(self, spotify_id):
        return self.request_data('/tracks/%s' % spotify_id, token=self.tok)

    def get_artist(self, spotify_id):
        return self.request_data('/artists/%s' % spotify_id, token=self.tok)

    def get_liked_songs(self, offset=0):
        return self.request_data('/me/tracks?limit=50&offset=%s' % offset, token=self.tok)

    def get_playlist_tracks(self, pid):
        return self.request_data('/playlists/%s/tracks' % pid, token=self.tok)["items"]

    def get_features(self, tid):
        return self.request_data('/audio-features/%s' % tid, token=self.tok)

    def search(self, query, type):
        query_list = query.split(" ")
        query_string = '%20'.join(query_list)
        return self.request_data(f'/search?q="{query_string}"&type={type}', token=self.tok)

    def search_track(self, query):
        return self.search(query, "track")

    def search_playlists(self, query):
        return self.search(query, "playlist")["playlists"]["items"]

    def create_playlist(self, uid, name):
        body = {"name": name}
        return self.request_data(f'/users/{uid}/playlists', method='POST', body=body, token=self.tok)['id']

    def add_tracks_to_playlist(self, playlist_id, track_ids):
        body_list = []
        track_string = f'spotify:track:{track_ids}'
        body_list.append(track_string)
        body = {"uris": body_list}
        return self.request_data(f'/playlists/{playlist_id}/tracks', method='POST', body=body, token=self.tok)

    def add_to_queue(self, uri):
        return self.request_data(f'/me/player/queue?uri={uri}', token=self.tok, method='POST', body=[])

    def skip(self):
        return self.request_data(f'/me/player/next', token=self.tok, method='POST', body=[])








