from flask import Flask, render_template
from get_home_runs import get_season_home_run_hitters, get_hr_stats, get_leaderboard
import os
import json

app = Flask(__name__)

@app.route("/")
def index():
    # Load players who hit HRs this season
    players = get_season_home_run_hitters()
    print(f"✅ Loaded {len(players)} players from cache")

    # Enrich each player with streak stats
    for p in players:
        try:
            streak_games, streak_abs = get_hr_stats(p["id"])
            p["games_since_hr"] = streak_games
            p["abs_since_hr"] = streak_abs
        except Exception as e:
            print(f"⚠️ Could not fetch HR streaks for {p['name']}: {e}")
            p["games_since_hr"] = "-"
            p["abs_since_hr"] = "-"

    # Load MLB stat leaderboard
    leaderboard = get_leaderboard()
    print(f"📊 Loaded {len(leaderboard)} stat leaders")

    # Merge leaderboard stats with HR streak info
    for player in leaderboard:
        match = next((p for p in players if p["id"] == player["id"]), None)
        if match:
            player["games_since_hr"] = match.get("games_since_hr", "-")
            player["abs_since_hr"] = match.get("abs_since_hr", "-")
        else:
            player["games_since_hr"] = "-"
            player["abs_since_hr"] = "-"

    return render_template("index.html", players=players, leaderboard=leaderboard)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
