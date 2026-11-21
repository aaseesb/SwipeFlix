from flask import Flask, render_template, jsonify, request
import scroll

app = Flask(__name__)


def render_card(state, movie, with_extras):
    kwargs = {}
    prob = 50
    if with_extras:
        prob = round(scroll.compute_like_probability(state, movie) * 100)
        fav = scroll.get_top_features(state)
        kwargs = dict(favGenre=fav['genres'], favDecade=fav['decade'],
                      favActor=fav['actors'], favMovie=fav['movie'])
    return render_template('movie.html',
                           movieName=movie.title,
                           releaseDate=movie.release_date[0:4],
                           movieGenre=", ".join(movie.genres),
                           movieDesc=movie.description,
                           movieCover=movie.cover,
                           movieRuntime=f"{movie.length//60}h, {movie.length%60}min",
                           movieCountry=movie.country,
                           movieActors=", ".join(movie.actors),
                           likeProb=prob,
                           **kwargs)


def start_state():
    state = scroll.new_state()
    state["queue"] = [m.title for m in scroll.select_initial_movies()]
    return state


@app.route('/')
def home():
    # the user's swipe state is handed to the browser, which sends it back with every swipe
    state = start_state()
    return render_template('home.html',
                           card=render_card(state, scroll.get_movie(state["queue"][0]), False),
                           state=state)


@app.route('/update_movie', methods=['POST'])
def updateMovie():
    data = request.get_json()
    liked_status = data.get('likedMovie') # true for accept, false for decline
    state = scroll.clean_state(data.get('state'))
    if not state["queue"]:
        state = start_state()

    old_movie = scroll.get_movie(state["queue"].pop(0))
    scroll.update_probability(state, old_movie, liked_status)
    state["queue"].append(scroll.select_movie_weighted(state).title)

    movie = scroll.get_movie(state["queue"][0])
    return jsonify(movie_html=render_card(state, movie, True), state=state)

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run(debug=False)
