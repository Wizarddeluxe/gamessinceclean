from flask import Flask, render_template
from get_home_runs import get_season_home_run_hitters, get_hr_stats
import os
import requests

app = Flask(__name__)

@app.route("/")
def index():
    players = get_season_home_run_hitters()
    leaderboard = []
    for p in players:
        try:
            games, abs_ = get_hr_stats(p["id"])
            p["games_since_hr"] = games
            p["abs_since_hr"] = abs_
        except:
            p["games_since_hr"] = "-"
            p["abs_since_hr"] = "-"
        leaderboard.append(p)
    leaderboard = sorted(leaderboard, key=lambda x: x.get("homeRuns", 0) if isinstance(x.get("homeRuns"), int) else 0, reverse=True)
    return render_template("index.html", leaderboard=leaderboard)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
