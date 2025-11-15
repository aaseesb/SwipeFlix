from flask import Flask, render_template
import scroll
query = []
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html',)


def update_query():
    if query == []:
        query = scroll.select_initial_movies()
    else:
        query.remove[0]
        query.append[scroll.select_movie_weighted()]


@app.route('/update_movie')
def updateMovie():
    new_movie = render_template('movie.html')
    return jsonify(new_movie);


if __name__ == '__main__':
    app.run(debug=False)