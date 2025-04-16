from flask import Flask, render_template
from get_home_runs import get_season_home_run_hitters, get_hr_stats
import os

app = Flask(__name__)

@app.route("/")
def index():
    players = get_season_home_run_hitters()
    print(f"✅ Loaded {len(players)} HR hitters from cache")

    # Add streak data for each player
    for p in players:
        try:
            streak_games, streak_abs = get_hr_stats(p["id"])
            p["games_since_hr"] = streak_games
            p["abs_since_hr"] = streak_abs
        except Exception as e:
            print(f"⚠️ Error with {p['name']}: {e}")
            p["games_since_hr"] = "-"
            p["abs_since_hr"] = "-"

    # Sort players by games since last HR (ascending)
    leaderboard = sorted(players, key=lambda x: (x["games_since_hr"] if isinstance(x["games_since_hr"], int) else 999))

    return render_template("index.html", players=players, leaderboard=leaderboard)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
