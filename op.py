from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

class User(db.Model):
    id = db.Column(db.String(), primary_key = True)
    name = db.Column(db.String(80), nullable = False)
    email = db.Column(db.String(40), nullable = False)
    password = db.Column(db.String(40), nullable = False)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('signup.html')
def signup():
    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)