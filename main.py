from colorama import init, Fore, Style
from requests import Response
import db
import json
import sys
import requests

# Inititialize colorama to fix formatted output on Windows
init(autoreset=True)

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
user_url: str = base_url + '/user/' + user + '/'
listening_url: str = user_url + 'playing-now'
listen_count_url: str = user_url + 'listen-count'

def get_response(url: str, isencapsulated: bool = True) -> dict:
    """Gets the JSON response from the URL, and parses it as a dictionary.\n
    Optionally takes a boolean to determine whether the response is encapsulated in the `payload` key.\n
    If the bool is true (default -- since most responses are), then the contents of the `payload` key is returned.\n
    Otherwise, the full response is returned."""
    response: Response = requests.get(url)
    json_dict: dict = json.loads(response.text)
    if isencapsulated:
        return json_dict['payload'] # All info is encapsulated in the `payload` key for most responses
    else:
        # But for the couple things that aren't encapsulated in the `payload` key, we can just pass False to the function
        return json_dict

def print_current_song():
    """Prints the current song being played."""
    useful_info: dict = get_response(listening_url)
    listens: dict = useful_info['listens']
    # If there are no elements in the list, then the user "is not listening to music"
    if len(listens) == 0:
        print('No music is being played currently, or your scrobbler is acting up.')
    # If there are elements in the list, then the user is listening to music
    else:
        # `listens` is an array which has everything in the first element
        listens = listens[0]
        # As you would expect, track metadata is in the `track_metadata` key
        track_metadata: dict = listens['track_metadata']
        artist_name: str = Fore.LIGHTWHITE_EX + Style.BRIGHT + track_metadata['artist_name'] + Style.RESET_ALL
        album_name: str = Fore.LIGHTCYAN_EX + Style.BRIGHT + track_metadata['release_name'] + Style.RESET_ALL
        track_name: str = Fore.LIGHTGREEN_EX + track_metadata['track_name']
        play_count: int = useful_info['count']
        print(f"Currently playing: {artist_name} - '{track_name}' on {album_name} [{play_count} play(s)]")

def print_total_play_count():
    """Prints the total number of plays the user has made."""
    useful_info: dict = get_response(listen_count_url)
    # The amount of songs the user has played
    listen_count: int = useful_info['count']
    print(f'{user} has listened to {listen_count} tracks.')

def print_similar_users():
    """Prints the users that are similar to the user, based on the listening history."""
    # Example: https://api.listenbrainz.org/1/stats/user/Phate6660/similar-users
    similar_users_url: str = user_url + '/similar-users'
    similar_users: dict = get_response(similar_users_url)
    # Sort the similar users by their similarity level (descending)
    similar_users.sort(key=lambda x: x['similarity'], reverse=True)
    # Add coloring to username
    colored_user = Fore.WHITE + Style.BRIGHT + user + Style.RESET_ALL
    # The similar users are an array of dictonaries containing the username and their similarity level
    for similar_user in similar_users:
        similar_user_name: str = Fore.WHITE + Style.BRIGHT + similar_user['user_name'] + Style.RESET_ALL
        similar_user_count: str = similar_user['similarity']
        if similar_user_count == 1.0:
            print(f'{similar_user_name} is a perfect match for {colored_user}!')
        else:
            # The similarity level is a float between 0 and 1
            # We want to color-code the similarity level to make it more visible, so
            # Anything over 0.75 is green, anything between 0.5 and 0.75 is yellow, and anything below 0.5 is red
            if similar_user_count > 0.75:
                similar_user_count = Fore.GREEN + Style.BRIGHT + str(similar_user_count) + Style.RESET_ALL
            elif similar_user_count > 0.5:
                similar_user_count = Fore.YELLOW + Style.BRIGHT + str(similar_user_count) + Style.RESET_ALL
            else:
                similar_user_count = Fore.RED + Style.BRIGHT + str(similar_user_count) + Style.RESET_ALL
            print(f'{similar_user_name} is {similar_user_count} times more similar to {colored_user}')

def print_artist_map():
    """Prints how many artists per country the user has listened to. Only shows countries with at least 1 listen."""
    # Example: https://api.listenbrinz.org/1/stats/user/Phate6660/artist-map
    artist_map_url: str = stats_base_url + 'user/' + user + '/artist-map'
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
        country_name: str = Fore.LIGHTBLACK_EX + Style.BRIGHT + country['country'] + Style.RESET_ALL
        country_count: str = Fore.WHITE + Style.BRIGHT + str(country['artist_count']) + Style.RESET_ALL
        print(f'{country_count} artists played in {country_name}')

def print_top_tracks():
    """Prints the top tracks the user has listened to, along with play counts."""
    # Example: https://api.listenbrainz.org/1/stats/user/Phate6660/recordings
    top_tracks_url: str = stats_base_url + 'user/' + user + '/recordings'
    useful_info: dict = get_response(top_tracks_url)
    # The top tracks are in the `recordings` key
    top_tracks: list = useful_info['recordings']
    # Sort the top tracks by the amount of times they have been played (descending)
    top_tracks.sort(key=lambda x: x['listen_count'], reverse=True)
    # The top tracks are an array of dictonaries containing the track name and the amount of times it has been played
    for track in top_tracks:
        track_name: str = Fore.WHITE + Style.BRIGHT + track['track_name'] + Style.RESET_ALL
        album_name: str = Fore.LIGHTBLACK_EX + track['release_name'] + Style.RESET_ALL
        artist_name: str = Fore.LIGHTBLACK_EX + Style.BRIGHT + track['artist_name'] + Style.RESET_ALL
        track_count: str = Fore.WHITE + Style.BRIGHT + str(track['listen_count']) + Style.RESET_ALL
        print(f'{track_count} times played: \'{track_name}\' on {album_name} by {artist_name}')

def print_top_releases():
    """Prints the top releases the user has listened to, along with play counts."""
    # Example: https://api.listenbrainz.org/1/stats/user/Phate6660/releases
    top_releases_url: str = stats_base_url + 'user/' + user + '/releases'
    useful_info: dict = get_response(top_releases_url)
    # The top releases are in the `releases` key
    top_releases: list = useful_info['releases']
    # Sort the top releases by the amount of times they have been played (descending)
    top_releases.sort(key=lambda x: x['listen_count'], reverse=True)
    # The top releases are an array of dictonaries containing the release name and the amount of times it has been played
    for release in top_releases:
        release_name: str = Fore.LIGHTBLACK_EX + Style.BRIGHT + release['release_name'] + Style.RESET_ALL
        artist_name: str = Fore.LIGHTBLACK_EX + Style.BRIGHT + release['artist_name'] + Style.RESET_ALL
        release_count: str = Fore.WHITE + Style.BRIGHT + str(release['listen_count']) + Style.RESET_ALL
        print(f'{release_count} times played: \'{release_name}\' by {artist_name}')

def print_top_artists():
    """Prints the top artists the user has listened to, along with play counts."""
    # Example: https://api.listenbrainz.org/1/stats/user/Phate6660/artists
    top_artists_url: str = stats_base_url + 'user/' + user + '/artists'
    useful_info: dict = get_response(top_artists_url)
    # The top artists are in the `artists` key
    top_artists: list = useful_info['artists']
    # Sort the top artists by the amount of times they have been played (descending)
    top_artists.sort(key=lambda x: x['listen_count'], reverse=True)
    # The top artists are an array of dictonaries containing the artist name and the amount of times they have been played
    for artist in top_artists:
        artist_name: str = Fore.LIGHTBLACK_EX + Style.BRIGHT + artist['artist_name'] + Style.RESET_ALL
        artist_count: int = Fore.WHITE + Style.BRIGHT + str(artist['listen_count']) + Style.RESET_ALL
        print(f'{artist_count} times played: \'{artist_name}\'')

def print_user_statistics(operation: str):
    """Prints the user's statistics based on the operation."""
    match operation:
        case 'artist-map':
            print_artist_map()
        case 'top-tracks':
            print_top_tracks()
        case 'top-releases':
            print_top_releases()
        case 'top-artists':
            print_top_artists()
        case _:
            print(f'{operation} is not a valid operation, please try one of: artist-map, top-tracks, top-releases, top-artists')

match op:
    case 'current':
        print_current_song()
    case 'count':
        print_total_play_count()
    case 'similar':
        print_similar_users()
    case 'stats':
        if argv_count == 3:
            print("Please enter an operation for user statistics. Currently supported is artist-map and top-tracks.")
            sys.exit(1)
        else:
            # Arg 3: Sub operation
            subop: str = sys.argv[3]
            print_user_statistics(subop)
    case _:
        print('Invalid operation. Valid operations are: current, count, and stats.')
        sys.exit(1)