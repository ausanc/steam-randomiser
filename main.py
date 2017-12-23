import argparse
import requests


def main():
    parser = argparse.ArgumentParser(description='Pick a random game from a user\'s Steam library.')
    parser.add_argument('user_id', help='the ID of the Steam account')
    args = parser.parse_args()

    with open("steam-api-key.txt", "r") as f:
        key = f.read()

    get_games_template = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={id}"
    url = get_games_template.format(**{"id": args.user_id, "key": key})
    print(url)

    r = requests.get(url)
    print(r.status_code)


if __name__ == "__main__":
    main()
