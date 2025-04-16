
def get_player_totals_from_logs(player_id):
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats?stats=gameLog&season=2025"
    try:
        r = requests.get(url)
        r.raise_for_status()
        logs = r.json()["stats"][0]["splits"]
        totals = {"homeRuns": 0, "hits": 0, "rbi": 0, "baseOnBalls": 0}
        
        if len(logs) == 0:  # If no data, return defaults for Ohtani or any player
            print(f"⚠️ No stats for player {player_id}")
            return totals
        
        for game in logs:
            stat = game["stat"]
            totals["homeRuns"] += int(stat.get("homeRuns", 0))
            totals["hits"] += int(stat.get("hits", 0))
            totals["rbi"] += int(stat.get("rbi", 0))
            totals["baseOnBalls"] += int(stat.get("baseOnBalls", 0))
        
        return totals
    except Exception as e:
        print(f"⚠️ Error aggregating logs for {player_id}: {e}")
        return {"homeRuns": "-", "hits": "-", "rbi": "-", "baseOnBalls": "-"}
