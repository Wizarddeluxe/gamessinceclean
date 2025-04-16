import requests
import json
from datetime import datetime

def get_all_games_with_dates(start_date, end_date):
    url = f"https://statsapi.mlb.com/api/v1/schedule?startDate={start_date}&endDate={end_date}&sportId=1"
    r = requests.get(url)
    dates = r.json().get("dates", [])
    game_entries = []
    for day in dates:
        date_str = day["date"]
        for game in day.get("games", []):
            game_entries.append({"gamePk": game["gamePk"], "date": date_str})
    return game_entries

def get_hr_hitters_from_game(game_id, date_str):
    url = f"https://statsapi.mlb.com/api/v1/game/{game_id}/boxscore"
    r = requests.get(url)
    data = r.json()
    players = []

    for team_type in ["home", "away"]:
        team = data["teams"][team_type]
        for pid, pdata in team["players"].items():
            stats = pdata.get("stats", {}).get("batting", {})
            if stats.get("homeRuns", 0) > 0:
                player = {
                    "id": pdata["person"]["id"],
                    "name": pdata["person"]["fullName"],
                    "last_hr_date": date_str
                }
                players.append(player)

    return players

def rebuild_hr_cache():
    print("🔁 Rebuilding full season HR cache...")
    start = "2025-03-28"
    end = datetime.today().strftime("%Y-%m-%d")

    game_entries = get_all_games_with_dates(start, end)
    print(f"📅 Found {len(game_entries)} games between {start} and {end}")

    seen_ids = set()
    hr_hitters = []

    for entry in game_entries:
        gid = entry["gamePk"]
        date_str = entry["date"]
        hitters = get_hr_hitters_from_game(gid, date_str)
        for h in hitters:
            if h["id"] not in seen_ids:
                seen_ids.add(h["id"])
                hr_hitters.append(h)

    hr_hitters = sorted(hr_hitters, key=lambda x: x["last_hr_date"], reverse=True)

    with open("data/season_hr_cache.json", "w") as f:
        json.dump(hr_hitters, f, indent=2)

    print(f"✅ Saved {len(hr_hitters)} unique HR hitters to data/season_hr_cache.json")

if __name__ == "__main__":
    rebuild_hr_cache()
