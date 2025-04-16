
import json
import requests

def get_season_home_run_hitters():
    with open("data/season_hr_cache.json") as f:
        return json.load(f)

def get_hr_stats(player_id):
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats?stats=gameLog&season=2025"
    r = requests.get(url)
    logs = r.json()["stats"][0]["splits"]
    
    if not logs:
        return "-", "-", "-", "-", "-", "-"

    hits = sum(int(g["stat"].get("hits", 0)) for g in logs)
    rbi = sum(int(g["stat"].get("rbi", 0)) for g in logs)
    walks = sum(int(g["stat"].get("baseOnBalls", 0)) for g in logs)
    home_runs = sum(int(g["stat"].get("homeRuns", 0)) for g in logs)

    last_hr_index = next((i for i, g in enumerate(logs) if int(g["stat"].get("homeRuns", 0)) > 0), None)

    if last_hr_index is None:
        return "-", "-", hits, rbi, walks, home_runs

    games_since_hr = last_hr_index
    abs_since_hr = sum(int(logs[i]["stat"].get("atBats", 0)) for i in range(last_hr_index))

    return games_since_hr, abs_since_hr, hits, rbi, walks, home_runs
