import os
import requests
from dotenv import load_dotenv
load_dotenv()

OMDB_API_KEY = os.environ.get("OMDB_API_KEY")
OMDB_URL = "https://www.omdbapi.com/"  

_omdb_cache = {}  


def fetch_omdb(title):
    if title in _omdb_cache:
        return _omdb_cache[title]

    if not OMDB_API_KEY:
        print("WARNING: OMDB_API_KEY not set!")
        return None  

    try:
        response = requests.get(
            OMDB_URL,
            params={"apikey": OMDB_API_KEY, "t": title},
            timeout=5
        )
        result = response.json()
    except requests.RequestException:
        _omdb_cache[title] = None
        return None

    if result.get("Response") == "True":
        info = {
            "poster": result.get("Poster"),
            "rating": result.get("imdbRating"),
            "actors": result.get("Actors"),
            "director": result.get("Director"),
            "year": result.get("Year"),
        }
    else:
        info = None  

    _omdb_cache[title] = info
    return info
