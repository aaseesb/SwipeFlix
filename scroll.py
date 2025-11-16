import json
import random
from math import log, exp

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
        self.decade = self.extract_decade(release_date)

    def extract_actor_names(self, actor_dict):
        # Combine lead and supporting actors into 1 list
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

feature_stats = {
    "genres": {},
    "actors": {},
    "country": {},
    "decade": {}
}

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

def compute_feature_weight(stats):
    likes = stats["likes"]
    dislikes = stats["dislikes"]
    return log(likes / dislikes)

def compute_movie_score(movie):
    score = 0
    for g in movie.genres:
        score += compute_feature_weight(feature_stats["genres"].get(g, {"likes":1,"dislikes":1}))
    for a in movie.actors:
        score += compute_feature_weight(feature_stats["actors"].get(a, {"likes":1,"dislikes":1}))
    score += compute_feature_weight(feature_stats["country"].get(movie.country, {"likes":1,"dislikes":1}))
    score += compute_feature_weight(feature_stats["decade"].get(movie.decade, {"likes":1,"dislikes":1}))
    return score

def compute_like_probability(movie):
    movies = []
    scores = []
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
        scores.append(compute_movie_score(m))
    
    exp_scores = [exp(s) for s in scores]
    total = sum(exp_scores)
    this_score = exp(compute_movie_score(movie))
    return this_score / total

def select_initial_movies():
    selected_movies = []
    for i in range(2):
        title_key = random.choice(list(movie_db.keys()))
        movie_info = movie_db[title_key]
        movie_obj = Movie(
            title=movie_info["title"],
            cover=movie_info["poster"],
            description=movie_info["description"],
            genres=movie_info["genres"],
            release_date=movie_info["release_date"],
            length=movie_info["runtime"],
            actors=movie_info["actors"],
            country=movie_info["country"],
            language=movie_info["language"]
        )
        selected_movies.append(movie_obj)
    return selected_movies

def select_movie_weighted():
    movies = []
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
    
    scores = [compute_movie_score(m) for m in movies]
    return random.choices(movies, weights=[exp(s) for s in scores], k=1)[0]
