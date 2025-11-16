import json
import random
from math import log, exp

starting_value = 100
decay_rate = 20
MIN_PROB = 50
MAX_PROB = 200

feature_stats = {
    "genres": {},
    "actors": {},
    "country": {},
    "decade": {}
}

with open("movies.json", "r", encoding='utf-8') as f:
    movie_db = json.load(f)

class Movie:
    def __init__(self, title, cover, description, genres, release_date, length, actors, country, language):
        self.title = title
        self.cover = cover
        self.description = description
        self.genres = genres
        self.release_date = release_date
        self.length = length
        self.actors = self.extract_actor_names(actors)
        self.country = country
        self.language = language
        self.decade = self.extract_decade(self.release_date)
        self.score = starting_value  # baseline score for probability

    def extract_actor_names(self, actor_dict):
        actors = []
        if "lead" in actor_dict and actor_dict["lead"]:
            actors.append(actor_dict["lead"])
        if "supporting" in actor_dict and actor_dict["supporting"]:
            actors.extend(actor_dict["supporting"])
        return actors

    def extract_decade(self, date_str):
        year = int(date_str.split("-")[0])
        decade = (year // 10) * 10
        return f"{decade}s"

def select_initial_movies():
    selected_movies = []
    for i in range(3):
        title_key = random.choice(list(movie_db.keys()))
        info = movie_db[title_key]
        m = Movie(
            title=info["title"],
            cover=info["poster"],
            description=info["description"],
            genres=info["genres"],
            release_date=info["release_date"],
            length=info["runtime"],
            actors=info["actors"],
            country=info["country"],
            language=info["language"]
        )
        selected_movies.append(m)
    return selected_movies

def update_feature(feature_dict, key, win):
    if key not in feature_dict:
        feature_dict[key] = {"likes": 1, "dislikes": 1}
    if win:
        feature_dict[key]["likes"] += 1
    else:
        feature_dict[key]["dislikes"] += 1

def update_probability(movie, win):
    # Update features
    for g in movie.genres:
        update_feature(feature_stats["genres"], g, win)
    for a in movie.actors:
        update_feature(feature_stats["actors"], a, win)
    update_feature(feature_stats["country"], movie.country, win)
    update_feature(feature_stats["decade"], movie.decade, win)

    # Update movie baseline score
    change = decay_rate if win else -decay_rate
    movie.score += change
    movie.score = max(MIN_PROB, min(MAX_PROB, movie.score))

MIN_PROB = 1
MAX_PROB = 99
BASE_PROB = 50 

def compute_like_probability(movie):
    prob = BASE_PROB

    for g in movie.genres:
        stats = feature_stats["genres"].get(g, {"likes": 1, "dislikes": 1})
        prob += log(stats["likes"] / stats["dislikes"]) * 5

    for a in movie.actors:
        stats = feature_stats["actors"].get(a, {"likes": 1, "dislikes": 1})
        prob += log(stats["likes"] / stats["dislikes"]) * 2

    stats = feature_stats["country"].get(movie.country, {"likes": 1, "dislikes": 1})
    prob += log(stats["likes"] / stats["dislikes"]) * 3

    stats = feature_stats["decade"].get(movie.decade, {"likes": 1, "dislikes": 1})
    prob += log(stats["likes"] / stats["dislikes"]) * 6

    prob = max(MIN_PROB, min(MAX_PROB, prob))

    return prob / 100

def select_movie_weighted():
    movies = []
    weights = []

    for info in movie_db.values():
        m = Movie(
            title=info["title"],
            cover=info["poster"],
            description=info["description"],
            genres=info["genres"],
            release_date=info["release_date"],
            length=info["runtime"],
            actors=info["actors"],
            country=info["country"],
            language=info["language"]
        )
        movies.append(m)
        weights.append(compute_like_probability(m))

    return random.choices(movies, weights=weights, k=1)[0]

"""
TEST SNIPPET

if __name__ == "__main__":
    print("Initial three random movies:")
    initial_movies = select_initial_movies()
    for m in initial_movies:
        print(f"- {m.title} ({m.decade})")

    print("\nSimulating 10 user likes:")
    for i in range(1, 15):
        movie = select_movie_weighted()
        win = True
        update_probability(movie, win)
        prob = compute_like_probability(movie)
        print(f"[Answer {i}] Liked: {movie.title} -> Probability: {prob*100:.2f}%")
"""