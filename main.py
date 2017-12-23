import argparse
import re
import requests


# tries to get a user_id from a provided vanity url name
def get_id_from_vanity(url_tokens):
    template = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={key}&vanityurl={vanity}"
    url = template.format(**url_tokens)
    r = requests.get(url)
    json = r.json()
    if json["response"]["success"] != 1:
        raise ValueError("Failed to get Steam ID from vanity name.")
    return json["response"]["steamid"]


def main():
    parser = argparse.ArgumentParser(description='Pick a random game from a user\'s Steam library.')
    parser.add_argument('user_id', help='the ID of the Steam account')
    args = parser.parse_args()

    # read key in from file
    with open("steam-api-key.txt", "r") as f:
        key = f.read()

    # if user_id is not in correct format, try getting the id from a vanity url
    if not re.match('^[0-9]{17}', args.user_id):
        args.user_id = get_id_from_vanity({"key": key, "vanity": args.user_id})


    get_owned_games = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={id}"
    url = get_owned_games.format(**{"id": args.user_id, "key": key})
    print(url)

    r = requests.get(url)
    print(r.status_code)


if __name__ == "__main__":
    main()
