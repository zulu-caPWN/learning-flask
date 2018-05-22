from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db
from forms import SignUpForm 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://127.0.0.1/learningflask'
db = SQLAlchemy(app)


app.secret_key = 'development-key' #csrf

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/signup")
def signup():
    form = SignUpForm()
    return render_template('signup.html', form=form)

if __name__ == "__main__":
  app.run(debug=True)