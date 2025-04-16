from flask import Flask, render_template
from get_home_runs import get_season_home_run_hitters, get_hr_stats
import os
import requests

app = Flask(__name__)

def get_player_totals(player_id):
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats?stats=season&season=2025"
    try:
        r = requests.get(url).json()
        stats = r["stats"][0]["splits"][0]["stat"]
        return {
            "homeRuns": int(stats.get("homeRuns", 0)),
            "hits": int(stats.get("hits", 0)),
            "rbi": int(stats.get("rbi", 0)),
            "baseOnBalls": int(stats.get("baseOnBalls", 0))
        }
    except Exception as e:
        print(f"⚠️ Failed to fetch stats for {player_id}: {e}")
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

        totals = get_player_totals(p["id"])
        p.update(totals)
        leaderboard.append(p)

    # Sort by HRs descending
    leaderboard = sorted(leaderboard, key=lambda x: x.get("homeRuns", 0) if isinstance(x.get("homeRuns"), int) else 0, reverse=True)

    return render_template("index.html", leaderboard=leaderboard, players=players)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
