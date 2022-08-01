import db
import json
import sys
import requests

argv_count: int = len(sys.argv)
# Missing first argument
if argv_count == 1:
    print("Please enter a username")
    sys.exit(1)
# Missing second argument
elif argv_count == 2:
    print("Please enter an operation")
    sys.exit(1)
# Arg 1: Username
user: str = sys.argv[1]
# Arg 2: Operation
op: str = sys.argv[2]
base_url: str = 'https://api.listenbrainz.org/1/'
stats_base_url: str = 'https://api.listenbrainz.org/1/stats/'
# Example: https://api.listenbrainz.org/1/user/Phate6660/
user_url: str = base_url + '/user/' + user + '/'
# Example: https://api.listenbrainz.org/1/user/Phate6660/playing-now
listening_url: str = user_url + 'playing-now'
# Example: https://api.listenbrainz.org/1/user/Phate6660/listen-count
listen_count_url: str = user_url + 'listen-count'
# Example: https://api.listenbrinz.org/1/stats/user/Phate6660/artist-map
artist_map_url: str = stats_base_url + 'user/' + user + '/artist-map'

def get_response(url) -> dict:
    """Gets the JSON response from the URL, parses it as a dictionary, and returns it starting from the `payload` key."""
    response = requests.get(url)
    json_dict = json.loads(response.text)
    return json_dict['payload'] # All info is encapsulated in the `payload` key

if op == 'current':
    useful_info: dict = get_response(listening_url)
    listens: dict = useful_info['listens']
    # If there are no elements in the list, then the user "is not listening to music"
    if len(listens) == 0:
        print('No music is being played currently, or your scrobbler is acting up.')
    # If there are elements in the list, then the user is listening to music
    else:
        # `listens` is an array which has everything in the first element
        listens: dict = listens[0]
        # As you would expect, track metadata is in the `track_metadata` key
        track_metadata: dict = listens['track_metadata']
        artist_name: str = track_metadata['artist_name']
        album_name: str = track_metadata['release_name']
        track_name: str = track_metadata['track_name']
        play_count: int = useful_info['count']
        print(f"Currently playing: {artist_name} - '{track_name}' on {album_name} [{play_count} play(s)]")
elif op == 'count':
    useful_info: dict = get_response(listen_count_url)
    # The amount of songs the user has played
    listen_count: int = useful_info['count']
    print(f'{user} has listened to {listen_count} tracks.')
elif op == 'stats':
    useful_info: dict = get_response(artist_map_url)
    # The artist map is in the `artist_map` key
    artist_map: dict = useful_info['artist_map']
    # Replace the 3-letter country codes with their full names in the artist map
    for country in artist_map:
        country_name: str = db.country_codes[country['country']]
        country['country'] = country_name
    # First sort the artist_map list alphabetically, then sort it by the amount of times the artist has been played (descending)
    artist_map.sort(key=lambda x: x['country'])
    artist_map.sort(key=lambda x: x['artist_count'], reverse=True)
    # The artist map is an array of dictonaries containing the country and the amount of artists played in that country
    # The countries are abbreviated to their 3-letter code
    for country in artist_map:
        country_name: str = country['country']
        country_count: int = country['artist_count']
        print(f'{country_count} artists played in {country_name}')
else:
    print('Invalid operation. Valid operations are: current, count, and stat.')
    sys.exit(1)