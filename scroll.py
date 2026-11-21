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


def new_state():
    """Per-user state. Lives in the browser and is sent with each request (the server is stateless)."""
    return {
        "queue": [],  # titles of the movies lined up for the user
        "seen": [],   # titles already swiped
        "explore": 0.3,
        "stats": {"genres": {}, "actors": {}, "country": {}, "decade": {}},
    }

def clean_state(raw):
    """Validate client-supplied state so bad input can't crash the scoring maths."""
    state = new_state()
    try:
        state["queue"] = [t for t in raw["queue"] if t in movie_db][:3]
        state["seen"] = [t for t in raw["seen"] if t in movie_db]
        state["explore"] = min(0.3, max(0.1, float(raw["explore"])))
        for cat, feats in raw["stats"].items():
            if cat in state["stats"]:
                for k, c in feats.items():
                    state["stats"][cat][str(k)] = {
                        "likes": max(1, int(c["likes"])), "dislikes": max(1, int(c["dislikes"]))}
    except (KeyError, TypeError, ValueError, AttributeError):
        return new_state()
    return state

with open("movies.json", "r", encoding='utf-8') as f:
    movie_db = json.load(f)
    copy_db = movie_db.copy()

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

def get_movie(title):
    info = movie_db[title]
    return Movie(
        title=info["title"], cover=info["poster"], description=info["description"],
        genres=info["genres"], release_date=info["release_date"], length=info["runtime"],
        actors=info["actors"], country=info["country"], language=info["language"])

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

def update_probability(state, movie, win):
    stats = state["stats"]
    for g in movie.genres:
        update_feature(stats["genres"], g, win)
    for a in movie.actors:
        update_feature(stats["actors"], a, win)
    update_feature(stats["country"], movie.country, win)
    update_feature(stats["decade"], movie.decade, win)
    state["seen"].append(movie.title)



MIN_PROB = 1
MAX_PROB = 99
BASE_PROB = 50 

def compute_like_probability(state, movie):
    feature_stats = state["stats"]
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

def select_movie_weighted(state):
    # movies the user hasn't swiped yet
    seen = set(state["seen"])
    pool = [info for title, info in movie_db.items() if title not in seen]

    # Exploration
    if random.random() < state["explore"]:
        info = random.choice(pool)
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
        state["explore"] = max(0.1, state["explore"] - 0.05)  # decay by 5%
        return movie

    # Exploitation
    best_movie = None
    best_prob = -1
    for info in pool:
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
        prob = compute_like_probability(state, m)
        if prob > best_prob:
            best_prob = prob
            best_movie = m

    return best_movie

def get_top_features(state):
    top_features = {}

    for category, stats in state["stats"].items():
        best_feature = None
        best_ratio = -1  # likes/dislikes ratio
        
        for feature, counts in stats.items():
            ratio = counts["likes"] / counts["dislikes"]
            if ratio > best_ratio:
                best_ratio = ratio
                best_feature = feature
        
        top_features[category] = best_feature
        
    best_movie = None
    best_score = -1

    for movie_id, info in copy_db.items():

        movie_genres = set(info["genres"])
        movie_actors = set(info["actors"]["supporting"] + 
                           ([info["actors"]["lead"]] if info["actors"]["lead"] else []))
        movie_country = info["country"]
        year = int(info["release_date"].split("-")[0])
        movie_decade = f"{(year // 10) * 10}s"

        score = 0
        if top_features["genres"] in movie_genres:
            score += 1
        if top_features["actors"] in movie_actors:
            score += 1
        if top_features["country"] == movie_country:
            score += 1
        if top_features["decade"] == movie_decade:
            score += 1

        if score > best_score:
            best_score = score
            best_movie = info

    top_features["movie"] = best_movie['title'] + " " + best_movie['release_date'][0:4]

    return top_features


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