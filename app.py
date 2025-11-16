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
                            releaseDate = movie.release_date,
                            movieGenre = movie.genres,
                            movieDesc = movie.description,
                            movieCover = movie.cover,
                            movieRuntime = movie.length,
                            movieCountry = movie.country,
                            movieActors = movie.actors
                            )

def update_query(liked_movie: bool):

    global query

    # FIRST TIME → fill queue
    if len(query) == 0:
        query.extend(scroll.select_initial_movies())
        return

    old_movie = query.pop(0)
    scroll.update_probability(old_movie, liked_movie)

    new_movie = scroll.select_movie_weighted()
    query.append(new_movie)
    
     # Compute & print probability for debugging
    prob = scroll.compute_like_probability(new_movie)
    print(f"[DEBUG] Selected: {new_movie.title} → Probability: {prob*100:.2f}%")

@app.route('/update_movie', methods=['POST'])
def updateMovie():
    data = request.get_json()
    liked_status = data.get('likedMovie') # true for accept, false for decline

    update_query(liked_status)
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