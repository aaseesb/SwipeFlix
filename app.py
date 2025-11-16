from flask import Flask, render_template, jsonify, request
import scroll

query = []
app = Flask(__name__)

@app.route('/')
def home():
    update_query()
    movie = query[0]

    return render_template('home.html', 
                            movieName = movie.title,
                            releaseDate = movie.release_date,
                            movieGenre = movie.genres,
                            movieDesc = movie.description,
                            movieCover = movie.cover,
                            movieRuntime = movie.length,
                            movieCountry = movie.country,
                            movieActors = movie.actors
                            )


def update_query():
    global query
    if query == []:
        query = scroll.select_initial_movies()
    else:
        query.pop(0)
        query.append(scroll.select_movie_weighted())


@app.route('/update_movie', methods=['POST'])
def updateMovie():
    data = request.get_json()
    liked_status = data.get('likedStatus') # decline or accept

    update_query(likedStatus)
    movie = query[0]

    page = render_template('movie.html', 
                            movieName = movie.title,
                            releaseDate = movie.release_date,
                            movieGenre = movie.genres,
                            movieDesc = movie.description,
                            movieCover = movie.cover,
                            movieRuntime = movie.length,
                            movieCountry = movie.country,
                            movieActors = movie.actors
                            )
    
    return jsonify(movie_html=page)


if __name__ == '__main__':
    app.run(debug=False)