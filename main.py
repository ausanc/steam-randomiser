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
    return steam_api_call_json(template, url_tokens)


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

    # if user_id is not in correct format, try getting the id from a vanity url
    if not re.match('^[0-9]{17}', args.user_id):
        args.user_id = get_id_from_vanity({"key": key, "vanity": args.user_id})

    # get games list, get list of unplayed games, pick one randomly and print
    owned_games_json = get_owned_games({"key": key, "id": args.user_id})
    owned_games = owned_games_json["response"]["games"]
    if args.all_games:
        selectable_games = [game["name"] for game in owned_games]
    else:
        selectable_games = [game["name"] for game in owned_games if game["playtime_forever"] <= args.time_played]
    print(random.choice(selectable_games))


if __name__ == "__main__":
    main()
