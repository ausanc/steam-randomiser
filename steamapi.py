import requests


def api_call_json(template, url_tokens):
    """Make a steam api call and return the json result, or throw a ValueError exception."""
    url = ("http://api.steampowered.com/" + template).format(**url_tokens)
    r = requests.get(url)
    
    if r.status_code != 200:
        raise ValueError("Status code of request is not 200.")
    return r.json()


def resolve_vanity_url(key, vanity):
    """Get a user_id from a provided vanity url name, or throw a ValueError exception."""
    template = "ISteamUser/ResolveVanityURL/v0001/?key={key}&vanityurl={vanity}"
    json = api_call_json(template, {"key": key, "vanity": vanity})
    if json["response"]["success"] != 1:
        raise ValueError("Failed to get Steam ID from vanity name.")
    return json["response"]["steamid"]


def get_owned_games(key, steam_id):
    """Get the list of owned games for a user."""
    template = "IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={id}&include_appinfo=1"
    json = api_call_json(template, {"key": key, "id": steam_id})
    if "games" not in json["response"]:
        raise ValueError("Failed to get games list for SteamID %s" % steam_id)
    return json["response"]["games"]


def get_global_achievement_percentages_for_app(game_id):
    template = "ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={game_id}"
    json = api_call_json(template, {"game_id": game_id})
    return json["achievementpercentages"]["achievements"]


def get_schema_for_game(key, app_id):
    template = "ISteamUserStats/GetSchemaForGame/v2/?key={key}&appid={app_id}"
    json = api_call_json(template, {"key": key, "app_id": app_id})
    return json
