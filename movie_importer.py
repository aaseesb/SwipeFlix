import requests
import json
import time
import os
import re 

API_KEY = "4dd92ae62b15a6c5ade7300d9f7c7ff9"
BASE = "https://api.themoviedb.org/3"

def fetch_movie_data(movie_name):
    """Fetch info for a single movie from TMDb."""
    try:
        search_url = f"{BASE}/search/movie?api_key={API_KEY}&query={movie_name}"
        search = requests.get(search_url).json()

        if not search.get("results"):
            print(f"No results for {movie_name}")
            return None

        movie = search["results"][0]
        movie_id = movie["id"]

        details_url = f"{BASE}/movie/{movie_id}?api_key={API_KEY}"
        details = requests.get(details_url).json()

        credits_url = f"{BASE}/movie/{movie_id}/credits?api_key={API_KEY}"
        credits = requests.get(credits_url).json()

        genres = [g["name"] for g in details.get("genres", [])]

        cast = credits.get("cast", [])
        lead = cast[0]["name"] if len(cast) > 0 else None
        supporting = [a["name"] for a in cast[1:3]] if len(cast) >= 3 else []

        countries = details.get("production_countries", [])
        country = countries[0]["name"] if countries else None

        return {
            "title": details.get("title"),
            "poster": f"https://image.tmdb.org/t/p/w500{details.get('poster_path')}" if details.get("poster_path") else None,
            "release_date": details.get("release_date"),
            "genres": genres,
            "language": details.get("original_language"),
            "description": details.get("overview"),
            "runtime": details.get("runtime"),
            "actors": {
                "lead": lead,
                "supporting": supporting
            },
            "country": country
        }

    except Exception as e:
        print(f"Error fetching {movie_name}: {e}")
        return None


def build_movie_database(movie_list, output_file='movies.json'):
    """Builds or updates a movie dictionary and saves it as JSON."""
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            database = json.load(f)
    else:
        database = {}

    # Add/update movies
    for name in movie_list:
        if name in database:
            print(f"{name} already exists in database, skipping.")
            continue
        print(f"Fetching {name}...")
        data = fetch_movie_data(name)
        if data:
            database[name] = data
        time.sleep(0.26)  # This delay is because the api only allows for 40 requests per 10 seconds. To avoid an error while loading a larger list a 0.26s offset is used to ensure 40 requests are never made in 10 seconds.

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(database, f, ensure_ascii=False, indent=4)

    print(f"Database saved as {output_file}")
    return database

with open("movie_importer_list.txt", 'r') as file:
    movie_list = file.read().splitlines()
    clean_movies = [re.sub(r'\s*\(\d{4}\)$', '', movie) for movie in movie_list]
    print(clean_movies)
    build_movie_database(clean_movies)
