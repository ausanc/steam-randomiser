import argparse
import random
import re
import requests


# make a steam api call and return the json result
def steam_api_call_json(template, url_tokens):
    url = template.format(**url_tokens)
    r = requests.get(url)
    if r.status_code != 200:
        raise ValueError("Status code of request is not 200.")
    return r.json()


# tries to get a user_id from a provided vanity url name
def get_id_from_vanity(url_tokens):
    template = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={key}&vanityurl={vanity}"
    json = steam_api_call_json(template, url_tokens)
    if json["response"]["success"] != 1:
        raise ValueError("Failed to get Steam ID from vanity name.")
    return json["response"]["steamid"]


# get the list of owned games for a user
def get_owned_games(url_tokens):
    template = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={id}&include_appinfo=1"
    return steam_api_call_json(template, url_tokens)["response"]["games"]


# accept multiple forms of user id input and return the 17 character form
def parse_id_input(id_input, api_key):
    if re.match(r'^[0-9]{17}$', id_input):  # if input matches correct form
        return id_input
    elif re.search(r'profiles/([0-9]{17})$', id_input):  # if using url with steamid64
        return re.search(r'profiles/([0-9]{17})$', id_input).group(1)
    elif re.search(r'id/(.*)$', id_input):  # if using url with vanity id
        vanity = re.search(r'id/(.*)$', id_input).group(1)
        return get_id_from_vanity({"key": api_key, "vanity": vanity})
    else:  # assume it is a vanity ID
        return get_id_from_vanity({"key": api_key, "vanity": id_input})


# picks a random game from a user's library
def pick_random_game(user_id, api_key, all_games=False, time_played=0):
    # convert user_id input into steam id 64 format
    steam_id_64 = parse_id_input(user_id, api_key)

    # get games list, get list of unplayed games, pick one randomly and print
    owned_games = get_owned_games({"key": api_key, "id": steam_id_64})
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
    parser.add_argument('-t', '--time_played', type=int, default=0,
        help='the time in minutes a game needs to have been played to count as played')
    args = parser.parse_args()

    # read key in from file
    with open("steam-api-key.txt", "r") as f:
        key = f.read()

    # get a random game from the user's library
    game = pick_random_game(args.user_id, key, all_games=args.all_games, time_played=args.time_played)
    print(game["name"])


if __name__ == "__main__":
    main()
