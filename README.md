# Steam Random Unplayed Game Picker
A small tool to pick a random unplayed game from a user's game library.

## Steam API Key
The program expects a file `steam-api-key.txt` containing just the API key.

## Command Line Arguments
`user_id`: program takes a profile's URL, a 17 digit steam ID, or a vanity URL ID.

Example: `python main.py https://steamcommunity.com/profiles/76561198033703131`, `python main.py https://steamcommunity.com/id/aviatorwest`, `python main.py 76561198033703131` or `python main.py aviatorwest` will all work.

`-a`, `--all_games`: Select from all games in the user's library, not just unplayed ones.

`-t`, `--time_played`: Change the threshold of how many minutes a game has to have been played for it to be excluded from the random selection. Use if you don't count a few minutes of playtime as really being played.

Example: `python main.py aviatorwest -t 10` will pick from all games with 10 minutes of playtime or less.
