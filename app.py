from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()  

from recommend import recommend, data  

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/titles")
def api_titles():
    titles = sorted(data["title"].tolist())
    return jsonify({"titles": titles})

@app.route("/api/recommend")
def api_recommend():
    print("OMDB_API_KEY present:", bool(os.environ.get("OMDB_API_KEY")))
    movie_name = request.args.get("movie", "").strip()
    if not movie_name:
        return jsonify({"error": "Please provide a movie name"}), 400

    outcome = recommend(movie_name)
    if outcome is None:
        return jsonify({"error": f'"{movie_name}" not found in dataset'}), 404

    return jsonify({
        "matched_title": movie_name,
        "results": outcome
    })


if __name__ == "__main__":
    app.run(debug=True)