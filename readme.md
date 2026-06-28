# 🎬 Movie Recommender

A content-based movie recommendation engine — type in a movie you like, get ten similar picks with real posters and IMDb ratings pulled live from OMDB.

## How it works

- Combines each movie's genres, keywords, overview, tagline, cast, and director into one text blob
- Cleans and tokenizes that text (regex + NLTK stopword removal)
- Vectorizes with TF-IDF (`scikit-learn`)
- Computes pairwise cosine similarity across every movie in the dataset
- Given a title, returns the top 10 most similar movies by similarity score
- Falls back to fuzzy matching (`difflib`) if the typed title isn't an exact match, so small typos still resolve
- Enriches each recommendation with a poster + rating from the OMDB API (cached, so repeat lookups don't burn API calls)

## Tech stack

- **Backend:** Python, Flask
- **ML / NLP:** pandas, scikit-learn (TF-IDF, cosine similarity), NLTK
- **External data:** OMDB API
- **Frontend:** vanilla HTML/CSS/JS (no framework)

## Project structure

```
movie-recommender/
├── app.py              # Flask app & API routes
├── recommend.py        # recommendation logic, loads model.pkl
├── omdb.py              # OMDB API wrapper with in-memory caching
├── train.py             # one-time script: builds model.pkl from movies.csv
├── model.pkl             # precomputed similarity matrix + movie data (gitignored)
├── movies.csv             # source dataset (gitignored — see Dataset section)
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── requirements.txt
```

## Setup

1. Clone the repo and `cd` into it
2. Create and activate a virtual environment
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Get a free OMDB API key: https://www.omdbapi.com/apikey.aspx
5. Create a `.env` file in the project root:
   ```
   OMDB_API_KEY=your_key_here
   ```
6. Download the dataset (see below) and place it as `movies.csv` in the project root
7. Build the model (run once, or again whenever `movies.csv` changes):
   ```bash
   python train.py
   ```
8. Run the app:
   ```bash
   python app.py
   ```
   Then open `http://127.0.0.1:5000`

## Dataset

This project expects a CSV with `title`, `genres`, `keywords`, `overview`, `tagline`, `cast`, and `director` columns — matching the structure of the TMDB 5000 Movies dataset. The dataset isn't included in this repo; download it separately and place it as `movies.csv` in the project root before running `train.py`.

## Known limitations

- Recommendations are based on metadata similarity (content-based filtering), not user behavior — two people who both like *Inception* will get the same suggestions
- OMDB's free tier caps at 1,000 requests/day
- Cast and director photos aren't shown, since OMDB only returns names, not images

## Possible next steps

- Hybrid filtering (blend content-based similarity with user ratings/collaborative signals)
- Deploy a live demo
- Swap in a different data source for cast/director photos

## License

MIT