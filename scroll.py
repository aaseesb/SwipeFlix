import json
import random
from math import log, exp


starting_value = 100
decay_rate = 20
MIN_PROB = 50
MAX_PROB = 200
GENRE_WEIGHT = 5
ACTOR_WEIGHT = 2
COUNTRY_WEIGHT = 0.5
DECADE_WEIGHT = 1
explore_rate = 0.3


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

    for g in movie.genres:
        update_feature(feature_stats["genres"], g, win)
    for a in movie.actors:
        update_feature(feature_stats["actors"], a, win)
    update_feature(feature_stats["country"], movie.country, win)
    update_feature(feature_stats["decade"], movie.decade, win)
    movie_db.pop(movie.title, None)



MIN_PROB = 1
MAX_PROB = 99
BASE_PROB = 50 

def compute_like_probability(movie):
    prob = BASE_PROB

    for g in movie.genres:
        stats = feature_stats["genres"].get(g, {"likes": 1, "dislikes": 1})
        prob += log(stats["likes"] / stats["dislikes"]) * GENRE_WEIGHT

    for a in movie.actors:
        stats = feature_stats["actors"].get(a, {"likes": 1, "dislikes": 1})
        prob += log(stats["likes"] / stats["dislikes"]) * ACTOR_WEIGHT

    stats = feature_stats["country"].get(movie.country, {"likes": 1, "dislikes": 1})
    prob += log(stats["likes"] / stats["dislikes"]) * COUNTRY_WEIGHT

    stats = feature_stats["decade"].get(movie.decade, {"likes": 1, "dislikes": 1})
    prob += log(stats["likes"] / stats["dislikes"]) * DECADE_WEIGHT

    prob = max(MIN_PROB, min(MAX_PROB, prob))

    return prob / 100

def select_movie_weighted():
    global explore_rate

    # Exploration
    if random.random() < explore_rate:
        info = random.choice(list(movie_db.values()))
        movie = Movie(
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
        explore_rate = max(0.1, explore_rate - 0.05)  # decay by 5%
        return movie

    # Exploitation
    best_movie = None
    best_prob = -1
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
        prob = compute_like_probability(m)
        if prob > best_prob:
            best_prob = prob
            best_movie = m

    return best_movie

def get_top_features():
    global feature_stats
    top_features = {}

    for category, stats in feature_stats.items():
        best_feature = None
        best_ratio = -1  # likes/dislikes ratio
        
        for feature, counts in stats.items():
            ratio = counts["likes"] / counts["dislikes"]
            if ratio > best_ratio:
                best_ratio = ratio
                best_feature = feature
        
        top_features[category] = best_feature
    
    return(top_features)

"""if __name__ == "__main__":
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
        print(f"[Answer {i}] Liked: {movie.title} -> Probability: {prob*100:.2f}%")"""
