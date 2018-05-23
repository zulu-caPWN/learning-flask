from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, User 
from forms import SignUpForm, LoginForm 
#import sensitive
#sensitive.py with sensitive.pyc is messing with hero, I must need to upload sensitive.pyc to heroku directly
#to make it work, for now we will keep it out.


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

            session['email'] = newuser.email
            return redirect(url_for('home'))
            #return 'Success'

    elif request.method == 'GET':
        return render_template('signup.html', form=form)


@app.route('/home')
def home():
    return render_template('home.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "POST":
        if form.validate() == False:
            return render_template("login.html", form=form)
        else:
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                session["email"] = form.email.data
                return redirect(url_for('home'))

            else:
                return redirect(url_for(login))

    elif request.method == "GET":
        return render_template("login.html", form=form)






if __name__ == "__main__":
  app.run(debug=True)