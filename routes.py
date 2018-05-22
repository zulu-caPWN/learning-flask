from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from models import db, User 
from forms import SignUpForm 
#import sensitive
#sensitive.py with sensitive.pyc 


app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = sensitive.psycopg_db_connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/learningflask'
db = SQLAlchemy(app)

#app.secret_key = sensitive.app_secret_key #csrf
app.secret_key = 'development-key' #csrf


@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if request.method == 'POST':
        
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()
            return 'Success'

    elif request.method == 'GET':
        return render_template('signup.html', form=form)

if __name__ == "__main__":
  app.run(debug=True)