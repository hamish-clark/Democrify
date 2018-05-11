
import sys
import json
import os
from spotipy import oauth2
import spotipy

spotifyAutho = json.load(open("spotifyAutho.txt"))

username     = spotifyAutho["username"]
client_id    = spotifyAutho["client_id"]
client_secret = spotifyAutho["client_secret"]
redirect_uri = spotifyAutho["redirect_uri"]
chosen_scope    ="user-modify-playback-state user-read-playback-state"


def prompt_for_user_token(username, scope=None, client_id = None,
        client_secret = None, redirect_uri = None, cache_path = None):
    ''' prompts the user to login if necessary and returns
        the user token suitable for use with the spotipy.Spotify 
        constructor

        Parameters:

         - username - the Spotify username
         - scope - the desired scope of the request
         - client_id - the client id of your app
         - client_secret - the client secret of your app
         - redirect_uri - the redirect URI of your app
         - cache_path - path to location to save tokens

    '''

    if not client_id:
        client_id = os.getenv('SPOTIPY_CLIENT_ID')

    if not client_secret:
        client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

    if not redirect_uri:
        redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

    if not client_id:
        print('''
            You need to set your Spotify API credentials. You can do this by
            setting environment variables like so:

            export SPOTIPY_CLIENT_ID='your-spotify-client-id'
            export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
            export SPOTIPY_REDIRECT_URI='your-app-redirect-url'

            Get your credentials at     
                https://developer.spotify.com/my-applications
        ''')
        raise spotipy.SpotifyException(550, -1, 'no credentials set')

    cache_path = cache_path or ".cache-" + username
    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, 
        scope=scope, cache_path=cache_path)

    # try to get a valid token for this user, from the cache,
    # if not in the cache, the create a new (this will send
    # the user to a web page where they can authorize this app)

    token_info = sp_oauth.get_cached_token()
    
    auth_url = sp_oauth.get_authorize_url()

    return (auth_url, sp_oauth)

def accessToken(sp_oauth, response):
        code = sp_oauth.parse_response_code(response)
        token_info = sp_oauth.get_access_token(code)
        if token_info:
            return token_info['access_token']
        else:
            return None 

def createLoginUrl():
    url, autho = prompt_for_user_token(username,
                                       chosen_scope,
                                       client_id=client_id,
                                       client_secret=client_secret,
                                       redirect_uri=redirect_uri)
    return (url, autho)

def get_spotify_service(token):
    service = spotipy.Spotify(auth=token)
    return service

def get_token(autho, response):
    return accessToken(autho, response)
    
def get_active_device(service):
    for device in service.devices()["devices"]:
        if device["is_active"] == True:
            return device
    
    return None


if __name__ == "__main__":
    url, autho = createLoginUrl()
    print(url)
    inp = input("Url: ")
    token = get_token(autho, inp)

    service = get_spotify_service(token)

    results = service.search("nikes", type = "track")["tracks"]["items"]

    pprint.pprint(results[0])
    

    
