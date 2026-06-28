import pickle
from omdb import fetch_omdb
import difflib

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

data = model["data"]
similarity = model["similarity"]

def recommend(movie_name, top_n=10):
    matches = data[data["title"].str.lower() == movie_name.lower()]

    if matches.empty:
        close = difflib.get_close_matches(movie_name, data["title"].tolist(), n=1, cutoff=0.6)
        if not close:
            return None
        matches = data[data["title"] == close[0]]

    idx = matches.index[0]
    matched_title = data.loc[idx, "title"]

    similarity_score = sorted(list(enumerate(similarity[idx])), key=lambda x: x[1], reverse=True)
    similarity_score = similarity_score[1:top_n + 1]
    movie_indices = [i[0] for i in similarity_score]
    results = data[["title", "tagline", "overview"]].iloc[movie_indices].to_dict("records")

    for movie in results:
        movie["omdb"] = fetch_omdb(movie["title"])
        print(movie)

    return {"matched_title": matched_title, "results": results}