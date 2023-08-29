from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movie-collection.db"
db.init_app(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    year = db.Column(db.Integer)
    description = db.Column(db.String, nullable=False)
    rating = db.Column(db.String, nullable=True)
    ranking = db.Column(db.String, nullable=False)
    review = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=False)


class MyForm(FlaskForm):
    movie_title = StringField('movie_title', validators=[DataRequired()])


with app.app_context():
    db.create_all()

all_movies = []


@app.route("/", methods=["GET", "POST"])
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    all_movies = result.scalars().all()

    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies=all_movies)




@app.route("/edit", methods=["GET", "POST"])
def editing():
    if request.method == "POST":
        movie_id = request.args["id"]
        movie_to_update = db.get_or_404(Movie, movie_id)
        movie_to_update.rating = request.form["rating"]
        movie_to_update.review = request.form["review"]
        db.session.commit()
        return redirect(url_for('home'))
    movie_id = request.args.get('id')
    movie_selected = db.get_or_404(Movie, movie_id)
    return render_template("edit.html", movies=movie_selected)

@app.route('/find', methods=["GET", "POST"])
def find():
    if request.method == "GET":
        title = request.args.get('title')
        img_url = request.args.get('img_url')
        years = request.args.get('year')
        description = request.args.get('description')
        rating = request.args.get('rating')
        year = years
        new_movie = Movie(
            title=title,
            year=year,
            description=description,
            rating=rating,
            ranking=0,
            review="None",
            img_url=img_url
        )
        with app.app_context():
            db.session.add(new_movie)
            db.session.commit()
        return redirect(url_for('home'))

@app.route("/delete", methods=["GET", "POST"])
def delete():
    movie_id = request.args.get('id')
    movie_to_delete = db.get_or_404(Movie, movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = MyForm()
    if form.validate_on_submit():
        params = {"t": form.movie_title.data,
                  "apikey": "910c4ff",
                  "page": 10}
        response = requests.get("http://www.omdbapi.com/", params=params)
        result = response.json()
        return render_template("select.html", results=result)
    return render_template("add.html", form=form)





if __name__ == '__main__':
    app.run(debug=True)
