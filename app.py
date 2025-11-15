from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', movieName="Interstellar")

if __name__ == '__main__':
    app.run(debug=False)