from flask import Flask, render_template, request
from bookclass import book_import


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=False)