import json
import random

starting_value = 100
decay_rate = 20

category_weights = {
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

    def extract_actor_names(self, actor_dict):
        #combine lead and support actors into 1 list
        actors = []

        if "lead" in actor_dict and actor_dict["lead"]:
            actors.append(actor_dict["lead"])

        if "supporting" in actor_dict and actor_dict["supporting"]:
            actors.extend(actor_dict["supporting"])

        return actors
    
    def extract_decade(self, date_str):
        # to qualify movies in the decade their released
        year = int(date_str.split("-")[0])
        decade = (year // 10) * 10
        return f"{decade}s"

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

def update_probability(movie, win):
    change = decay_rate if win else -decay_rate

    for g in movie.genres:
        category_weights["genres"][g] = category_weights["genres"].get(g, starting_value) + change

    for a in movie.actors:
        category_weights["actors"][a] = category_weights["actors"].get(a, starting_value) + change

    c = movie.country
    category_weights["country"][c] = category_weights["country"].get(c, starting_value) + change

    d = movie.decade
    category_weights["decade"][d] = category_weights["decade"].get(d, starting_value) + change

def compute_movie_score(movie):
    score = 0

    for g in movie.genres:
        score += category_weights["genres"].get(g, starting_value)

    for a in movie.actors:
        score += category_weights["actors"].get(a, starting_value)

    score += category_weights["country"].get(movie.country, starting_value)

    score += category_weights["decade"].get(movie.decade, starting_value)

    return score

def select_movie_weighted():
    movies = []

    for key, info in movie_db.items():
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

    weights = [compute_movie_score(m) for m in movies]

    return random.choices(movies, weights=weights, k=1)[0]