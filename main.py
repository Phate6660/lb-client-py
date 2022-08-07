from colorama import init
from consts import argv_count, op, user, \
    country_codes, listening_url, listening_activity_url, \
    daily_activity_url, listen_count_url, listens_url, \
    similar_users_url, artist_map_url, top_artists_url, \
    top_releases_url, top_tracks_url, LightBlack, \
    LightCyan, LightGreen, LightWhite, \
    White, Yellow, Green, Red
import datetime
import json
from shared_functions import get_response
import sys
import requests

# Inititialize colorama to fix formatted output on Windows
init(autoreset=True)

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
        artist_name: str = LightWhite.Apply(track_metadata['artist_name'])
        album_name: str = LightCyan.Apply(track_metadata['release_name'])
        track_name: str = LightGreen.Apply(track_metadata['track_name'])
        play_count: int = useful_info['count']
        print(f"Currently playing: {artist_name} - '{track_name}' on {album_name} [{play_count} play(s)]")

def print_total_play_count():
    """Prints the total number of plays the user has made."""
    # Example: https://api.listenbrainz.org/1/user/Phate6660/listen-count
    useful_info: dict = get_response(listen_count_url)
    # The amount of songs the user has played
    listen_count: int = useful_info['count']
    print(f'{user} has listened to {listen_count} tracks.')

def print_listens(total: int = 0):
    """Prints the listens of the user.\n
    Will optionally take a number of listens to show.\n
    Defaults to 0 for infinite."""
    if total != 0:
        # Limit the listen count to the number of listens specified
        response = requests.get(listens_url, params={'count': total})
        listens: dict = json.loads(response.text)['payload']
    else:
        # Get all listens
        listens: dict = get_response(listens_url)
    # The listens are in the `listens` key
    listens = listens['listens']
    # Sort the listens by the date they were played (descending)
    listens.sort(key=lambda x: x['listened_at'], reverse=True)
    # The listens are an array of dictonaries containing the track, artist, album, and date (in unix epoch timestamp format) they were played
    for listen in listens:
        # Metadata is in the `track_metadata` key
        metadata = listen['track_metadata']
        track_name: str = LightBlack.Apply(metadata['track_name'])
        artist_name: str = LightBlack.Apply(metadata['artist_name'])
        album_name: str = LightCyan.Apply(metadata['release_name'])
        date: str = LightWhite.Apply(str(datetime.datetime.fromtimestamp(listen['listened_at'])))
        print(f'{date} - {artist_name} - {track_name} on {album_name}')

def print_similar_users():
    """Prints the users that are similar to the user, based on the listening history."""
    similar_users: dict = get_response(similar_users_url)
    # Sort the similar users by their similarity level (descending)
    similar_users.sort(key=lambda x: x['similarity'], reverse=True)
    # Add coloring to username
    colored_user = White.Apply(user)
    # The similar users are an array of dictonaries containing the username and their similarity level
    for similar_user in similar_users:
        similar_user_name: str = White.Apply(similar_user['user_name'])
        similar_user_count: str = similar_user['similarity']
        if similar_user_count == 1.0:
            print(f'{similar_user_name} is a perfect match for {colored_user}!')
        else:
            # The similarity level is a float between 0 and 1
            # We want to color-code the similarity level to make it more visible, so
            # Anything over 0.75 is green, anything between 0.5 and 0.75 is yellow, and anything below 0.5 is red
            if similar_user_count > 0.75:
                similar_user_count = Green.Apply(str(similar_user_count))
            elif similar_user_count > 0.5:
                similar_user_count = Yellow.Apply(str(similar_user_count))
            else:
                similar_user_count = Red.Apply(str(similar_user_count))
            print(f'{similar_user_name} is {similar_user_count} times more similar to {colored_user}')

def print_artist_map():
    """Prints how many artists per country the user has listened to. Only shows countries with at least 1 listen."""
    useful_info: dict = get_response(artist_map_url)
    # The artist map is in the `artist_map` key
    artist_map: dict = useful_info['artist_map']
    # Replace the 3-letter country codes with their full names in the artist map
    for country in artist_map:
        country_name: str = country_codes[country['country']]
        country['country'] = country_name
    # First sort the artist_map list alphabetically, then sort it by the amount of times the artist has been played (descending)
    artist_map.sort(key=lambda x: x['country'])
    artist_map.sort(key=lambda x: x['artist_count'], reverse=True)
    # The artist map is an array of dictonaries containing the country and the amount of artists played in that country
    # The countries are abbreviated to their 3-letter code
    for country in artist_map:
        country_name: str = LightBlack.Apply(country['country'])
        country_count: str = White.Apply(str(country['artist_count']))
        print(f'{country_count} artists played in {country_name}')

def print_top_tracks():
    """Prints the top tracks the user has listened to, along with play counts."""
    # Example: https://api.listenbrainz.org/1/stats/user/Phate6660/recordings
    useful_info: dict = get_response(top_tracks_url)
    # The top tracks are in the `recordings` key
    top_tracks: list = useful_info['recordings']
    # Sort the top tracks by the amount of times they have been played (descending)
    top_tracks.sort(key=lambda x: x['listen_count'], reverse=True)
    # The top tracks are an array of dictonaries containing the track name and the amount of times it has been played
    for track in top_tracks:
        track_name: str = White.Apply(track['track_name'])
        album_name: str = LightBlack.Apply(track['release_name'])
        artist_name: str = LightBlack.Apply(track['artist_name'])
        track_count: str = White.Apply(str(track['listen_count']))
        print(f'{track_count} times played: \'{track_name}\' on {album_name} by {artist_name}')

def print_top_releases():
    """Prints the top releases the user has listened to, along with play counts."""
    # Example: https://api.listenbrainz.org/1/stats/user/Phate6660/releases
    useful_info: dict = get_response(top_releases_url)
    # The top releases are in the `releases` key
    top_releases: list = useful_info['releases']
    # Sort the top releases by the amount of times they have been played (descending)
    top_releases.sort(key=lambda x: x['listen_count'], reverse=True)
    # The top releases are an array of dictonaries containing the release name and the amount of times it has been played
    for release in top_releases:
        release_name: str = LightBlack.Apply(release['release_name'])
        artist_name: str = LightBlack.Apply(release['artist_name'])
        release_count: str = White.Apply(str(release['listen_count']))
        print(f'{release_count} times played: \'{release_name}\' by {artist_name}')

def print_top_artists():
    """Prints the top artists the user has listened to, along with play counts."""
    useful_info: dict = get_response(top_artists_url)
    # The top artists are in the `artists` key
    top_artists: list = useful_info['artists']
    # Sort the top artists by the amount of times they have been played (descending)
    top_artists.sort(key=lambda x: x['listen_count'], reverse=True)
    # The top artists are an array of dictonaries containing the artist name and the amount of times they have been played
    for artist in top_artists:
        artist_name: str = LightBlack.Apply(artist['artist_name'])
        artist_count: int = White.Apply(str(artist['listen_count']))
        print(f'{artist_count} times played: \'{artist_name}\'')

def print_listening_activity():
    """Prints the user's listening activity over the course of a year for multiple years.\n
    TODO: Add support for refining the range."""
    useful_info: dict = get_response(listening_activity_url)
    # The listening activity is in the `listening_activity` key
    listening_activity: dict = useful_info['listening_activity']
    for listen in listening_activity:
        listen_count: str = LightBlack.Apply(str(listen['listen_count']))
        from_timestamp: str = LightBlack.Apply(datetime.datetime.fromtimestamp(listen['from_ts']).strftime('%d/%m/%Y'))
        to_timestamp: str = LightBlack.Apply(datetime.datetime.fromtimestamp(listen['to_ts']).strftime('%d/%m/%Y'))
        print(f'{listen_count} listens from {from_timestamp} to {to_timestamp}')

def print_daily_activity():
    """Prints the user's daily listening activity.\n
    TODO: The range for the daily activity seems to be a bit extreme. Add refining of the range."""
    useful_info: dict = get_response(daily_activity_url)
    from_ts = datetime.datetime.fromtimestamp(useful_info['from_ts']).strftime('%d/%m/%Y')
    to_ts = datetime.datetime.fromtimestamp(useful_info['to_ts']).strftime('%d/%m/%Y')
    # The daily activity is in the `daily_activity` key
    daily_activity: dict = useful_info['daily_activity']
    print(f'This info is from {from_ts} to {to_ts}.')
    for day in daily_activity:
        day_list = daily_activity[day]
        for actual_day in day_list:
            listen_count: str = LightBlack.Apply(str(actual_day['listen_count']))
            hour: str = LightBlack.Apply(str(actual_day['hour']))
            colored_day = LightBlack.Apply(day)
            print(f'{listen_count} listens at hour {hour} on {colored_day}')

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
        case 'listening-activity':
            print_listening_activity()
        case 'daily-activity':
            print_daily_activity()
        case _:
            print(
f"'{operation}' is not a valid operation, please try one of:\n\
* artist-map\n\
* top-tracks\n\
* top-releases\n\
* top-artists\n\
* listening-activity\n\
* daily-activity"
            )

match op:
    case 'current':
        print_current_song()
    case 'count':
        print_total_play_count()
    case 'listens':
        if argv_count == 4:
            count: int = int(sys.argv[3])
            print_listens(count)
        else:
            print_listens()
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