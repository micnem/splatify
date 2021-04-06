from django.shortcuts import render, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from requests import Request, post
from .models import Artist, TopArtist, RelatedArtist, Profile
from django.utils import timezone
from datetime import timedelta
import requests as r
import json
import  base64
from splatify2.settings import CLIENT_ID, CLIENT_SECRET

BASE_URL = "https://api.spotify.com/v1/"

def execute_spotify_api_request(access_token, endpoint, post_=False, put_=False):
    
    headers = {'Content-Type': 'application/json',
               'Authorization': "Bearer " + access_token}

    if post_:
        r.post(BASE_URL + endpoint, headers=headers)
    if put_:
        r.put(BASE_URL + endpoint, headers=headers)

    response = r.get(BASE_URL + endpoint, {}, headers=headers)
    try:
        return response.json()
    except:
        return {'Error': 'Issue with request'}

def create_artist(items):
    artist_list = []
  
    for item in items:
        spotify_id = item.get('id')
        # image = item.get('images')[0].get('url')
        name = item.get('name')
        popularity = item.get('popularity')
        uri = item.get('uri')

        artist = {
            'spotify_id': spotify_id,
            'name': name,
            # 'image': image,
            'popularity': popularity,
            'uri': uri
        }

        artist_list.append(artist)
    
    return artist_list


def get_top_artists(profile):
    access_token = refresh_tokens(profile)
    endpoint = "me/top/artists?time_range=long_term&limit=20"
    response = execute_spotify_api_request(access_token, endpoint)

    if response == None:
        endpoint = "me/top/artists?time_range=short_term&limit=20"
        response = execute_spotify_api_request(access_token, endpoint)

    items = response.get('items')
    artist_list = create_artist(items)

    for num, artist in enumerate(artist_list[::-1]):
        current_artist, created = Artist.objects.get_or_create(name = artist['name'], spotify_id = artist['spotify_id'], popularity = artist['popularity'], uri = artist['uri'])
        endpoint = f"artists/{current_artist.spotify_id}/related-artists"
        response = execute_spotify_api_request(access_token, endpoint)
        items = response.get('artists')

        rel_artist_list = create_artist(items)
    

        for number, rel_artist in enumerate(rel_artist_list[::-1]):
            related_artist, created = Artist.objects.get_or_create(name = rel_artist['name'], spotify_id = rel_artist['spotify_id'], popularity = rel_artist['popularity'], uri = rel_artist['uri'])
            RelatedArtist.objects.get_or_create(root_artist=current_artist, artist2=related_artist, affinity=number + 1)


        ta, created = TopArtist.objects.get_or_create(artist=current_artist, profile=profile, affinity=num+1)
        
    profile.populated = True
    profile.save()
    


def match(user_list):
    master_artist_list = []
    for num, user in enumerate(user_list):
        top_artists = user.profile.fave_artists.all()
        related_artists = RelatedArtist.objects.filter(root_artist__in = top_artists).distinct().values_list("artist2", flat=True)
        artist_list = (Artist.objects.filter(id__in = related_artists)|top_artists).distinct()
        if num == 0:
            master_artist_list = artist_list
        else:
            master_artist_list = master_artist_list.intersection(artist_list)

    return master_artist_list
    
def create_playlist(profile, user2):
    access_token = refresh_tokens(profile)
    user_id = profile.account.social_auth.first().uid
    endpoint = f"users/{user_id}/playlists"
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + access_token}
    body = json.dumps({
          "name": f"SplatList for {profile.account.first_name} and {user2.first_name}",
          "description": "A playlist generated for you, by Splatify, with love.",
          "public": False
        })
    response = r.post(BASE_URL + endpoint, body, headers=headers)
    playlist_id = response.json()
    return playlist_id['id']

    

def add_to_playlist(profile, track_uri_list, playlist_id):
    access_token = refresh_tokens(profile)
    track_urls = '%2c'.join(track_uri_list)
    endpoint = f"playlists/{playlist_id}/tracks?uris=" + track_urls
    response = execute_spotify_api_request(access_token, endpoint, post_=True)
    return response
   

def get_artist_top_songs(artist, profile):
    access_token = refresh_tokens(profile)
    artist_id = artist.spotify_id
    endpoint = f"artists/{artist_id}/top-tracks?country=IL"
    response = execute_spotify_api_request(access_token, endpoint)

    tracks = response['tracks']
    track_uri_list = []
    while len(track_uri_list)<3:
        for track in tracks:
            track_uri_list.append(track['uri'])
    
    return track_uri_list

def main(master_artist_list, profile, user2):
    master_artist_list = master_artist_list[0:20]
    playlist_id = create_playlist(profile, user2)
    if len(master_artist_list) > 5:
        for artist in master_artist_list:
            add_to_playlist(profile, get_artist_top_songs(artist, profile), playlist_id)
    else:
        track_uri_list = seeder(master_artist_list, profile)
        add_to_playlist(profile, track_uri_list, playlist_id)

def refresh_tokens(profile):
    endpoint = "https://accounts.spotify.com/api/token"
    refresh_token = profile.account.social_auth.first().extra_data['refresh_token']
    auth_str = '{}:{}'.format(CLIENT_ID, CLIENT_SECRET)
    b64_auth_str = base64.urlsafe_b64encode(auth_str.encode()).decode()
    headers = {'Authorization': f'Basic  {b64_auth_str}'}
    body = {
        'grant_type': 'refresh_token',
        'refresh_token':refresh_token,
    }
    response = r.post(endpoint, body, headers=headers)
    return response.json()['access_token']

def seeder(artist_list, profile):
    seed_artists = []
    for artist in artist_list:
        seed_artists.append(artist.spotify_id)
    seed_artists = seed_artists[:5]
    artists = '%2c'.join(seed_artists)
    endpoint = f"recommendations?seed_artists=" + artists
    access_token = refresh_tokens(profile)
    headers = {'Content-Type': 'application/json',
               'Authorization': "Bearer " + access_token}
    response = r.get(BASE_URL + endpoint, headers = headers)
    track_uri_list = []

    if response.json()['error']['status'] == 400:
        track_uri_list.append('spotify:track:4uLU6hMCjMI75M1A2tKUQC')
    else:
        rec_tracks = response.json()['tracks']
        
        
        for track in rec_tracks:
            track_uri_list.append(track['uri'])

    return track_uri_list

def artist_search(query, profile):
    access_token = refresh_tokens(profile)
    endpoint = f"https://api.spotify.com/v1/search?q={query}&type=artist"
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer " + access_token}
    response = r.get(endpoint, headers = headers)
    artist = response.json()['artists']['items'][0]

    current_artist, created = Artist.objects.get_or_create(name = artist['name'], spotify_id = artist['id'], popularity = artist['popularity'], uri = artist['uri'])
    TopArtist.objects.get_or_create(profile=profile, artist=current_artist, affinity=30)
    
    return current_artist

