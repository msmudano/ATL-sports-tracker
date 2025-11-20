from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

@app.route("/")
def index():
    data = load_data()
    falcons_data = data.get("falcons", {})
    hawks_data = data.get("hawks", {})
    gt_data = data.get("gt", {})
    return render_template("index.html", falcons_data=falcons_data, 
                           hawks_data=hawks_data, 
                           gt_data=gt_data)

@app.route("/falcons")
def falcons():
    data = load_data()
    falcons_data = data.get("falcons", {})
    return render_template("falcons.html", falcons_data=falcons_data)

@app.route("/georgia_tech_fb")
def gt():
    data = load_data()
    gt_data = data.get("gt", {})
    return render_template("gt.html", gt_data=gt_data)

@app.route("/hawks")
def hawks():
    data = load_data()
    hawks_data = data.get("hawks", {})
    return render_template("hawks.html", hawks_data=hawks_data)

@app.route("/georgia_tech_bb")
def gt_bb():
    data = load_data()
    gt_bb_data = data.get("gt_bb", {})
    return render_template("gt_bb.html", gt_bb_data=gt_bb_data)

@app.route("/api/data")
def api_data():
    data = load_data()
    return jsonify(data)

if __name__ == "__main__":
    # For local dev only: debug=True auto-reloads on changes
    app.run(host="127.0.0.1", port=5000, debug=True)
