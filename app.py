from flask import Flask, render_template
import os
import json

app = Flask(__name__)

@app.route("/")
def index():
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        cache_path = os.path.join(BASE_DIR, "data", "season_hr_cache.json")
        with open(cache_path, "r") as f:
            players = json.load(f)
            print(f"✅ Loaded {len(players)} players from season_hr_cache.json")
            if players:
                print(f"✅ Example player: {players[0]['name']}")
    except Exception as e:
        print(f"❌ Failed to load HR cache: {e}")
        players = []

    return render_template("index.html", players=players, leaderboard=[])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
