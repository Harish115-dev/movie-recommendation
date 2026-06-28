
import pandas as pd
import re
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download("stopwords")
nltk.download("punkt")
nltk.download("punkt_tab")

stop_words = set(stopwords.words("english"))

def preprocess(text):
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [w for w in tokens if w not in stop_words]
    return " ".join(tokens)

data = pd.read_csv("movies.csv")
data = data.dropna(subset=["title"]).reset_index(drop=True)


feature_cols = ["genres", "keywords", "overview", "tagline", "cast", "director"]
for col in feature_cols:
    data[col] = data[col].fillna("")

combined = (data["genres"] + " " + data["keywords"] + " " + data["overview"]
            + " " + data["tagline"] + " " + data["cast"] + " " + data["director"])
movie_text = data["title"] + " " + combined

movie_text = movie_text.apply(preprocess)  

vectorizer = TfidfVectorizer(max_features=5000)
vectors = vectorizer.fit_transform(movie_text)

similarity = cosine_similarity(vectors, vectors).astype("float32")

slim_data = data[["title", "tagline", "overview"]].reset_index(drop=True)

with open("model.pkl", "wb") as f:
    pickle.dump({"data": slim_data, "similarity": similarity}, f)

print(f"Saved model.pkl — {len(slim_data)} movies, similarity shape {similarity.shape}")