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
    games = 0
    abs_ = 0
    for game in logs:
        games += 1
        abs_ += int(game["stat"].get("atBats", 0))
        if int(game["stat"].get("homeRuns", 0)) > 0:
            break
    return games, abs_
