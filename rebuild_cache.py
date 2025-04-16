
import requests, json
from datetime import datetime

def get_all_games_with_dates(start_date, end_date):
    url = f"https://statsapi.mlb.com/api/v1/schedule?startDate={start_date}&endDate={end_date}&sportId=1"
    r = requests.get(url)
    dates = r.json().get("dates", [])
    return [{"gamePk": game["gamePk"], "date": day["date"]} for day in dates for game in day.get("games", [])]

def get_hr_hitters_from_game(game_id, date_str):
    url = f"https://statsapi.mlb.com/api/v1/game/{game_id}/boxscore"
    r = requests.get(url)
    data = r.json()
    players = []
    for team_type in ["home", "away"]:
        for pdata in data["teams"][team_type]["players"].values():
            stats = pdata.get("stats", {}).get("batting", {})
            if stats.get("homeRuns", 0) > 0:
                players.append({"id": pdata["person"]["id"], "name": pdata["person"]["fullName"], "last_hr_date": date_str})
    return players

def rebuild_hr_cache():
    start, end = "2025-03-28", datetime.today().strftime("%Y-%m-%d")
    seen, result = set(), []
    for entry in get_all_games_with_dates(start, end):
        for h in get_hr_hitters_from_game(entry["gamePk"], entry["date"]):
            if h["id"] not in seen:
                seen.add(h["id"])
                result.append(h)
    result = sorted(result, key=lambda x: x["last_hr_date"], reverse=True)
    with open("data/season_hr_cache.json", "w") as f:
        json.dump(result, f, indent=2)
    print(f"✅ Saved {len(result)} HR hitters")

if __name__ == "__main__":
    rebuild_hr_cache()
