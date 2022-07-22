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
# Example: https://api.listenbrainz.org/1/user/Phate6660/
user_url = base_url + '/user/' + user + '/'
# Example: https://api.listenbrainz.org/1/user/Phate6660/playing-now
listening_url = user_url + 'playing-now'
# Example: https://api.listenbrainz.org/1/user/Phate6660/listen-count
listen_count_url = user_url + 'listen-count'

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
else:
    print('Invalid operation. Valid operations are: current, count.')
    sys.exit(1)