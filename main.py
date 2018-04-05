#!/usr/bin/env python3
import argparse
import random
import re
import requests


def steam_api_call_json(template, url_tokens):
    """Make a steam api call and return the json result, or throw a ValueError exception."""
    url = template.format(**url_tokens)
    r = requests.get(url)
    if r.status_code != 200:
        raise ValueError("Status code of request is not 200.")
    return r.json()


def get_id_from_vanity(key, vanity):
    """Get a user_id from a provided vanity url name, or throw a ValueError exception."""
    template = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={key}&vanityurl={vanity}"
    json = steam_api_call_json(template, {"key": key, "vanity": vanity})
    if json["response"]["success"] != 1:
        raise ValueError("Failed to get Steam ID from vanity name.")
    return json["response"]["steamid"]


def get_owned_games(key, steam_id):
    """Get the list of owned games for a user."""
    template = \
        "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={id}&include_appinfo=1"
    return steam_api_call_json(template, {"key": key, "id": steam_id})["response"]["games"]


def parse_id_input(id_input, api_key):
    """Accept multiple forms of user id input and return the 17 character form."""
    if re.match(r'^[0-9]{17}$', id_input):  # if input matches correct form
        return id_input
    elif re.search(r'profiles/([0-9]{17})$', id_input):  # if using url with steamid64
        return re.search(r'profiles/([0-9]{17})$', id_input).group(1)
    elif re.search(r'id/(.*)$', id_input):  # if using url with vanity id
        vanity = re.search(r'id/(.*)$', id_input).group(1)
        return get_id_from_vanity(api_key, vanity)
    else:  # assume it is a vanity ID
        return get_id_from_vanity(api_key, id_input)


def pick_random_game(key, user_id, all_games=False, time_played=0):
    """Pick a random game from a user's library."""
    # convert user_id input into steam id 64 format
    steam_id = parse_id_input(user_id, key)

    # get games list, get list of unplayed games, pick one randomly and print
    owned_games = get_owned_games(key, steam_id)
    if all_games:
        selectable_games = owned_games
    else:
        selectable_games = [game for game in owned_games if game["playtime_forever"] <= time_played]

    return random.choice(selectable_games)


def main():
    # command line arg handling
    parser = argparse.ArgumentParser(description='Pick a random game from a user\'s Steam library.')
    parser.add_argument('user_id', help='the ID of the Steam account')
    parser.add_argument('-a', '--all_games', help='pick from all games, not just unplayed ones', action='store_true')
    parser.add_argument(
        '-t', '--time_played', type=int, default=0,
        help='the time in minutes a game needs to have been played to count as played'
    )
    args = parser.parse_args()

    # read key in from file
    with open("steam-api-key.txt", "r") as f:
        key = f.read().strip()

    # get a random game from the user's library
    game = pick_random_game(key, args.user_id, all_games=args.all_games, time_played=args.time_played)
    print(game["name"])


if __name__ == "__main__":
    main()
