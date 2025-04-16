from flask import Flask, render_template
from get_home_runs import get_season_home_run_hitters, get_hr_stats
import os

app = Flask(__name__)

@app.route("/")
def index():
    players = get_season_home_run_hitters()
    leaderboard = []
    for p in players:
        try:
            games_since_hr, abs_since_hr, hits, rbis, walks, home_runs = get_hr_stats(p["id"])
            p["games_since_hr"] = games_since_hr
            p["abs_since_hr"] = abs_since_hr
            p["hits"] = hits
            p["rbi"] = rbis
            p["baseOnBalls"] = walks
            p["homeRuns"] = home_runs
        except:
            p["games_since_hr"] = "-"
            p["abs_since_hr"] = "-"
            p["hits"] = "-"
            p["rbi"] = "-"
            p["baseOnBalls"] = "-"
            p["homeRuns"] = "-"
        leaderboard.append(p)
    leaderboard = sorted(leaderboard, key=lambda x: x.get("homeRuns", 0) if isinstance(x.get("homeRuns"), int) else 0, reverse=True)
    return render_template("index.html", leaderboard=leaderboard)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))