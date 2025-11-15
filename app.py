from flask import Flask, render_template, jsonify
import scroll

query = []
app = Flask(__name__)

@app.route('/')
def home():
    updateMovie()
    return render_template('home.html',)


def update_query():
    global query
    if query == []:
        query = scroll.select_initial_movies()
    else:
        query.pop[0]
        query.append(scroll.select_movie_weighted())


@app.route('/update_movie')
def updateMovie():
    update_query()
    movie = query[0]
    page = render_template('movie.html', 
                           movieName = movie.title,
                           releaseDate = movie.release_date,
                           movieGenre = movie.genres,
                           movieDesc = movie.description,
                           movieCover = movie.cover,
                           movieRuntime = movie.length,
                           movieCountry = movie.country,
                           movieLanguage = movie.language,
                           movieActors = movie.actors
                           )
    return jsonify(page)


if __name__ == '__main__':
    app.run(debug=False)