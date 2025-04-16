from flask import Flask, render_template
from get_home_runs import get_season_home_run_hitters, get_hr_stats
import os
import requests

app = Flask(__name__)

def get_player_totals_from_logs(player_id):
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats?stats=gameLog&season=2025"
    try:
        r = requests.get(url)
        r.raise_for_status()
        logs = r.json()["stats"][0]["splits"]
        totals = {
            "homeRuns": 0,
            "hits": 0,
            "rbi": 0,
            "baseOnBalls": 0
        }
        for game in logs:
            stat = game["stat"]
            totals["homeRuns"] += int(stat.get("homeRuns", 0))
            totals["hits"] += int(stat.get("hits", 0))
            totals["rbi"] += int(stat.get("rbi", 0))
            totals["baseOnBalls"] += int(stat.get("baseOnBalls", 0))
        return totals
    except Exception as e:
        print(f"⚠️ Error aggregating logs for {player_id}: {e}")
        return {
            "homeRuns": "-",
            "hits": "-",
            "rbi": "-",
            "baseOnBalls": "-"
        }

@app.route("/")
def index():
    players = get_season_home_run_hitters()
    print(f"✅ Loaded {len(players)} HR hitters from cache")

    leaderboard = []

    for p in players:
        try:
            streak_games, streak_abs = get_hr_stats(p["id"])
            p["games_since_hr"] = streak_games
            p["abs_since_hr"] = streak_abs
        except Exception as e:
            print(f"⚠️ Error with {p['name']} streaks: {e}")
            p["games_since_hr"] = "-"
            p["abs_since_hr"] = "-"

        season_totals = get_player_totals_from_logs(p["id"])
        p.update(season_totals)
        leaderboard.append(p)

    leaderboard = sorted(
        leaderboard,
        key=lambda x: x.get("homeRuns", 0) if isinstance(x.get("homeRuns"), int) else 0,
        reverse=True
    )

    return render_template("index.html", leaderboard=leaderboard, players=players)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
