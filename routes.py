from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Place 
from forms import SignUpForm, LoginForm, AddressForm 
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

    if 'email' in session:
        return redirect(url_for('home'))

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


@app.route('/home', methods=["POST", "GET"])
def home():
    if 'email' not in session:
        return redirect(url_for('login'))
    form = AddressForm()

    places = []
    my_coordinates = (37.4221, -122.0844) #just dflts, mean nothing
    if request.method == "POST":
        if form.validate == False:
            return render_template('home.html', form=form)
        else:
            # get the addy
            address = form.address.data 
            # make a model to wrap or consume the wiki api then query it at https://www.mediawiki.org/wiki/Extension:GeoData#Api
            p = Place()
            my_coordinates = p.address_to_latlng(address)
            places = p.query(address)
            # return results
            return render_template('home.html', form=form, my_coordinates=my_coordinates, places=places)
    elif request.method == "GET":
        return render_template('home.html', form=form, my_coordinates=my_coordinates, places=places)

@app.route("/login", methods=["GET", "POST"])
def login():
    if 'email' in session:
        return redirect(url_for('home'))
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

@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))




if __name__ == "__main__":
  app.run(debug=True)