import json
import requests

def fetch_players_with_home_runs():
    url = "https://statsapi.mlb.com/api/v1/stats/leaders?leaderCategories=homeRuns&season=2025&limit=300"
    r = requests.get(url)
    
    # Print out the full response to understand the structure
    response_json = r.json()
    print(json.dumps(response_json, indent=2))  # Pretty print the JSON response for debugging
    
    # Adjusting this logic to match the structure of the API response
    players = []
    try:
        for p in response_json["leagueLeaders"][0]["leaders"]:
            players.append({
                "id": p["player"]["id"],
                "name": p["player"]["fullName"]
            })
    except KeyError as e:
        print(f"KeyError: {e} - check the API response structure.")
        return []
    
    return players

if __name__ == "__main__":
    players = fetch_players_with_home_runs()
    with open("data/season_hr_cache.json", "w") as f:
        json.dump(players, f)
    print(f"✅ Cached {len(players)} HR hitters.")

