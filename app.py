from flask import Flask, render_template
from get_home_runs import get_season_home_run_hitters, get_hr_stats, get_leaderboard
import os

app = Flask(__name__)

@app.route("/")
def index():
    players = get_season_home_run_hitters()
    print(f"✅ Loaded {len(players)} HR hitters from cache")

    # Enrich players with streak data
    for p in players:
        try:
            streak_games, streak_abs = get_hr_stats(p["id"])
            p["games_since_hr"] = streak_games
            p["abs_since_hr"] = streak_abs
        except Exception as e:
            print(f"⚠️ Error with {p['name']}: {e}")
            p["games_since_hr"] = "-"
            p["abs_since_hr"] = "-"

    # Pull full stat leaderboard
    leaderboard_raw = get_leaderboard()
    print(f"📊 Loaded {len(leaderboard_raw)} from get_leaderboard()")

    leaderboard = []
    used_ids = set()

    for entry in leaderboard_raw:
        if entry["id"] in used_ids:
            continue
        used_ids.add(entry["id"])
        # Try to find streak info from player list
        match = next((p for p in players if p["id"] == entry["id"]), None)
        if match:
            entry["games_since_hr"] = match.get("games_since_hr", "-")
            entry["abs_since_hr"] = match.get("abs_since_hr", "-")
        else:
            entry["games_since_hr"] = "-"
            entry["abs_since_hr"] = "-"
        leaderboard.append(entry)

    # Sort by HRs descending
    leaderboard = sorted(leaderboard, key=lambda x: x.get("homeRuns", 0), reverse=True)

    return render_template("index.html", leaderboard=leaderboard, players=players)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
