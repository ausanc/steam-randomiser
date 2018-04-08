#!/usr/bin/env python3
import argparse
import random
import re
import steamapi


def parse_id_input(id_input, api_key):
    """Accept multiple forms of user id input and return the 17 character form."""
    if re.match(r'^[0-9]{17}$', id_input):  # if input matches correct form
        return id_input
    elif re.search(r'profiles/([0-9]{17})$', id_input):  # if using url with steamid64
        return re.search(r'profiles/([0-9]{17})$', id_input).group(1)
    elif re.search(r'id/(.*)$', id_input):  # if using url with vanity id
        vanity = re.search(r'id/(.*)$', id_input).group(1)
        return steamapi.resolve_vanity_url(api_key, vanity)
    else:  # assume it is a vanity ID
        return steamapi.resolve_vanity_url(api_key, id_input)


def pick_random_game(key, user_id, all_games=False, time_played=0):
    """Pick a random game from a user's library."""
    # convert user_id input into steam id 64 format
    steam_id = parse_id_input(user_id, key)

    # get games list, get list of unplayed games, pick one randomly and print
    owned_games = steamapi.get_owned_games(key, steam_id)
    if all_games:
        selectable_games = owned_games
    else:
        selectable_games = [game for game in owned_games if game["playtime_forever"] <= time_played]

    return random.choice(selectable_games)


def get_random_achievement(key, appid, cutoff=80):
    achievements = steamapi.get_global_achievement_percentages_for_app(appid)
    if len(achievements) == 0:
        print("No achievements for this game")
        return None

    schema = steamapi.get_schema_for_game(key, appid)
    schema_achievements = schema["game"]["availableGameStats"]["achievements"]
    modifier = 100.0 / achievements[0]["percent"]
    candidates = [achievement for achievement in achievements if achievement["percent"] * modifier >= cutoff]
    for item in schema_achievements:
        for stat in achievements:
            if item["name"] == stat["name"]:
                item["percent"] = stat["percent"]
                break

    sorted_by_unlocked = reversed(sorted(schema_achievements, key=lambda tup: tup["percent"]))
    for achievement in sorted_by_unlocked:
        print("%s: %.1f%%" % (achievement["displayName"].encode("ascii", errors='replace').decode("ascii"), achievement["percent"]))

    random_cheevo_name = random.choice(candidates)["name"]
    found_display_name = ""
    for item in schema_achievements:
        if item["name"] == random_cheevo_name:
            found_display_name = item["displayName"]
    return found_display_name


def main():
    # command line arg handling
    parser = argparse.ArgumentParser(description='Pick a random game from a user\'s Steam library.')
    parser.add_argument('user_id', help='the ID of the Steam account')
    parser.add_argument('-a', '--all_games', help='pick from all games, not just unplayed ones', action='store_true')
    parser.add_argument(
        '-t', '--time_played', type=int, default=0,
        help='the time in minutes a game needs to have been played to count as played'
    )
    parser.add_argument('-c', '--achievement', help='pick a random achievement as an objective', action='store_true')
    args = parser.parse_args()

    # read key in from file
    with open("steam-api-key.txt", "r") as f:
        key = f.read().strip()

    # get a random game from the user's library
    game = pick_random_game(key, args.user_id, all_games=args.all_games, time_played=args.time_played)
    print("App ID: %s" % game["appid"])
    print(game["name"])
    if args.achievement:
        print("Challenge achievement: %s" % get_random_achievement(key, game["appid"]))


if __name__ == "__main__":
    main()
