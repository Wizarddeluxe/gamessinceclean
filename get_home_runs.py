
import json
import os
import requests

def get_season_home_run_hitters():
    with open("data/season_hr_cache.json") as f:
        return json.load(f)

def get_hr_stats(player_id):
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats?stats=gameLog&season=2025"
    r = requests.get(url)
    logs = r.json()["stats"][0]["splits"]
    
    if not logs:  # Check if no game logs are returned
        print(f"⚠️ No data for player {player_id}")
    
    games = 0
    abs_ = 0
    hits = 0
    rbis = 0
    walks = 0
    home_runs = 0
    last_hr_game = None  # Track the last HR game

    # Iterate through all games to calculate stats
    for game in logs:
        games += 1
        abs_ += int(game["stat"].get("atBats", 0))
        hits += int(game["stat"].get("hits", 0))
        rbis += int(game["stat"].get("rbi", 0))
        walks += int(game["stat"].get("baseOnBalls", 0))
        home_runs += int(game["stat"].get("homeRuns", 0))
        
        # Track last HR game
        if int(game["stat"].get("homeRuns", 0)) > 0:
            last_hr_game = game["date"]
            break  # Stop after finding the last HR hit game
    
    if last_hr_game:
        # Count the number of games since the last HR and ABs since that HR
        games_since_hr = 0
        abs_since_hr = 0
        for game in logs:
            if game["date"] > last_hr_game:
                games_since_hr += 1
                abs_since_hr += int(game["stat"].get("atBats", 0))
        
        return games_since_hr, abs_since_hr, hits, rbis, walks, home_runs
    else:
        return "-", "-", hits, rbis, walks, home_runs
