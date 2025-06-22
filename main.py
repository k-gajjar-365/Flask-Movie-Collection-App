from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os

# TMDb API details
API_KEY = os.environ.get("API_KEY_TMDB")
end_point = "https://api.themoviedb.org/3/search/movie"

# App initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY_APP")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies-list.db"
bs = Bootstrap5(app)

# SQLAlchemy setup with declarative base
class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Movie(db.Model):
    """Represents a movie entry in the database."""
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


class ReviewEditForm(FlaskForm):
    """Form for editing a movie's rating and review."""
    rating = StringField('Your rating out of 10 e.g. 7.5', validators=[DataRequired()])
    review = StringField('Your review', validators=[DataRequired()])
    submit = SubmitField("Done")


class AddMovieForm(FlaskForm):
    """Form for adding a movie by searching its title."""
    title = StringField('Movie title', validators=[DataRequired()])
    rating = StringField("Rating out of 10")
    review = StringField("Review")
    submit = SubmitField("Add a movie")


# Uncomment these blocks to initialize the DB and add a sample movie
# with app.app_context():
#     db.create_all()
#
# with app.app_context():
#     new_movie = Movie(
#         title="Phone Booth",
#         year=2002,
#         description="Publicist Stuart Shepard finds himself trapped in a phone booth...",
#         rating=7.3,
#         ranking=10,
#         review="My favourite character was the caller.",
#         img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
#     )
#     db.session.add(new_movie)
#     db.session.commit()

movie_list = []

@app.route("/")
def home():
    """
    Displays the home page with all movies sorted by rating (descending).
    Assigns dynamic ranking based on rating order.
    """
    global movie_list
    result = db.session.execute(db.select(Movie).order_by(Movie.rating.desc()))
    movie_list = result.scalars().all()

    # Re-rank movies based on current rating order
    for rank, movie in enumerate(movie_list, start=1):
        movie.ranking = rank
        db.session.commit()

    return render_template("index.html", movie=movie_list)


@app.route("/edit", methods=["GET", "POST"])
def edit_rating():
    """
    Displays and handles the rating/review edit form for a specific movie.
    """
    form = ReviewEditForm()
    movie_id = request.args.get("id")
    selected_movie = db.get_or_404(Movie, movie_id)

    if form.validate_on_submit():
        selected_movie.rating = float(form.rating.data)
        selected_movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=form, movie=selected_movie)


@app.route('/del')
def delete_movie():
    """
    Deletes a movie from the database by ID and redirects to home.
    """
    movie_id = request.args.get('id')
    Movie.query.filter_by(id=movie_id).delete()
    db.session.commit()
    return redirect(url_for('home'))


# Temporary global variables (replace with session-based logic in production)
rating = None
review = None

@app.route('/add', methods=["POST", "GET"])
def insert_movie():
    """
    Handles the movie addition form:
    - On GET: displays form
    - On POST: searches TMDb for the entered title and collects user input (rating/review)
    """
    form = AddMovieForm()
    if request.method == "GET":
        return render_template('add.html', form=form)
    elif request.method == "POST":
        para = {
            "query": request.form.get('title'),
            "api_key": API_KEY
        }
        global rating, review
        rating = request.form.get("rating")
        review = request.form.get("review")

        response = requests.get(end_point, params=para).json()
        return render_template("select.html", data=response, form=form)


@app.route('/select')
def find():
    """
    Finalizes the movie addition:
    - Fetches full details of the selected movie from TMDb
    - Creates and stores a new Movie object in the database
    """
    para = {
        "api_key": API_KEY,
        "language": "en-US"
    }
    movie_id = request.args.get("id")
    data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}", params=para).json()
    poster_path = data['poster_path']
    new_movie = Movie(
        title=data["title"],
        year=int(data["release_date"].split("-")[0]),  # Extracts just the year
        description=data["overview"],
        img_url=f"https://image.tmdb.org/t/p/original/{poster_path}",
        rating=float(rating) if rating else None,
        ranking=0,
        review=review
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
