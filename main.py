import db
import json
import sys
import requests

argv_count = len(sys.argv)
if argv_count == 1:
    print("Please enter a username")
    sys.exit(1)
elif argv_count == 2:
    print("Please enter an operation")
    sys.exit(1)
# Arg 1: Username
user = sys.argv[1]
# Arg 2: Operation
op = sys.argv[2]
base_url = 'https://api.listenbrainz.org/1/'
stats_base_url = 'https://api.listenbrainz.org/1/stats/'
# Example: https://api.listenbrainz.org/1/user/Phate6660/
user_url = base_url + '/user/' + user + '/'
# Example: https://api.listenbrainz.org/1/user/Phate6660/playing-now
listening_url = user_url + 'playing-now'
# Example: https://api.listenbrainz.org/1/user/Phate6660/listen-count
listen_count_url = user_url + 'listen-count'
# Example: https://api.listenbrinz.org/1/stats/user/Phate6660/artist-map
artist_map_url = stats_base_url + 'user/' + user + '/artist-map'

if op == 'current':
    # Get the response from the API
    playingnow_response = requests.get(listening_url)
    # Load the JSON response into a Python dictionary
    json_dict = json.loads(playingnow_response.text)
    # All of the info is stuck in the payload key
    useful_info = json_dict['payload']
    # The boolean which indicates if the user is listening to music
    playing_now = useful_info['playing_now']
    # Most info we want is in the `listens` key
    listens = useful_info['listens']
    # If there are no elements in the list, then the user "is not listening to music"
    if len(listens) == 0:
        print('No music is being played currently, or your scrobbler is acting up.')
    # If there are elements in the list, then the user is listening to music
    else:
        # `listens` is an array which has everything in the first element
        listens = listens[0]
        # As you would expect, track metadata is in the `track_metadata` key
        track_metadata = listens['track_metadata']
        artist_name = track_metadata['artist_name']
        album_name = track_metadata['release_name']
        track_name = track_metadata['track_name']
        play_count = useful_info['count']
        print(f"Currently playing: {artist_name} - '{track_name}' on {album_name} [{play_count} play(s)]")
elif op == 'count':
    # Get the response from the API
    listen_count_response = requests.get(listen_count_url)
    # Load the JSON response into a Python dictionary
    json_dict = json.loads(listen_count_response.text)
    # All of the info is stuck in the payload key
    useful_info = json_dict['payload']
    # The amount of songs the user has played
    listen_count = useful_info['count']
    print(f'{user} has listened to {listen_count} tracks.')
elif op == 'stats':
    # Get the response from the API
    artist_map_response = requests.get(artist_map_url)
    # Load the JSON response into a Python dictionary
    json_dict = json.loads(artist_map_response.text)
    # All of the info is stuck in the payload key
    useful_info = json_dict['payload']
    # The artist map is in the `artist_map` key
    artist_map = useful_info['artist_map']
    # Replace the 3-letter country codes with their full names in the artist map
    for country in artist_map:
        country_name = db.country_codes[country['country']]
        country['country'] = country_name
    # First sort the artist_map list alphabetically, then sort it by the amount of times the artist has been played (descending)
    artist_map.sort(key=lambda x: x['country'])
    artist_map.sort(key=lambda x: x['artist_count'], reverse=True)
    # The artist map is an array of dictonaries containing the country and the amount of artists played in that country
    # The countries are abbreviated to their 3-letter code
    for country in artist_map:
        country_name = country['country']
        country_count = country['artist_count']
        print(f'{country_count} artists played in {country_name}')
else:
    print('Invalid operation. Valid operations are: current, count.')
    sys.exit(1)