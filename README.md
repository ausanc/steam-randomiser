# Steam Random Unplayed Game Picker
A small tool to pick a random unplayed game from a user's game library.

## Steam API Key
The program expects a file `steam-api-key.txt` containing just the API key.

## Command Line Arguments
`user_id`: program takes a profile's URL, a 17 digit steam ID, or a vanity URL ID.

Example: `python strandom.py https://steamcommunity.com/profiles/76561198033703131`, `python strandom.py https://steamcommunity.com/id/ausanc`, `python strandom.py 76561198033703131` or `python strandom.py ausanc` are all valid.

`-a`, `--all_games`: Select from all games in the user's library, not just unplayed ones.

`-t`, `--time_played`: Change the threshold of how many minutes a game has to have been played for it to be excluded from the random selection. Use if you don't count a few minutes of playtime as really being played. Default: 0.

Example: `python strandom.py ausanc -t 10` will pick from all games with 10 minutes of playtime or less.

`-v`, `--achievement`: Select a random achievement from the picked game as an objective to complete.

`-c`, `--cutoff`: Set the cutoff percentage for the randomly chosen achievement. Default: 80.

Example: `python strandom.py ausanc -v -c 60` will randomly select a game, then randomly select an achievement which has been unlocked by at least 60% of players. The unlocked percentage is modified so that the most common achievement's percentage becomes the new 100%, to handle differences in achievement stats between different games.
