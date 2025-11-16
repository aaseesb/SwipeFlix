from flask import Flask, render_template, jsonify, request
import scroll

query = []
app = Flask(__name__)

@app.route('/')
def home():
    update_query(True)
    movie = query[0]

    return render_template('home.html', 
                            movieName = movie.title,
                            releaseDate = movie.release_date[0:4],
                            movieGenre = ", ".join(movie.genres),
                            movieDesc = movie.description,
                            movieCover = movie.cover,
                            movieRuntime = f"{movie.length//60}h, {movie.length%60}min" ,
                            movieCountry = movie.country,
                            movieActors = ", ".join(movie.actors)
                            likeProb = 50%
                            )

def update_query(liked_movie: bool):

    global query

    # fill queue for first time
    if len(query) == 0:
        query.extend(scroll.select_initial_movies())
        return

    old_movie = query.pop(0)
    scroll.update_probability(old_movie, liked_movie)

    new_movie = scroll.select_movie_weighted()
    query.append(new_movie)
    

@app.route('/update_movie', methods=['POST'])
def updateMovie():
    data = request.get_json()
    liked_status = data.get('likedMovie') # true for accept, false for decline
    
    update_query(liked_status)
    movie = query[0]


    # compute probability
    prob = scroll.compute_like_probability(movie)
    prob_percent = round(prob * 100)


    page = render_template('movie.html', 
                            movieName = movie.title,
                            releaseDate = movie.release_date[0:4],
                            movieGenre = ", ".join(movie.genres),
                            movieDesc = movie.description,
                            movieCover = movie.cover,
                            movieRuntime = f"{movie.length//60} hours, {movie.length%60} min" ,
                            movieCountry = movie.country,
                            movieActors = ", ".join(movie.actors),
                            likeProb = prob_percent
                            )
    
    return jsonify(movie_html=page)


if __name__ == '__main__':
    app.run(debug=False)