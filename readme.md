# 🎬 Flask Movie Collection App

A [Flask](https://flask.palletsprojects.com/en/stable/)-based web application to manage your favorite movies. Add, edit, delete, and rank movies using data fetched from [TMDb API](https://www.themoviedb.org/documentation/api). Styled with [Bootstrap](https://getbootstrap.com/) and powered by [SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/en/stable/) ORM.

---

## 🚀 Features

- Search movies via TMDb and add them to your collection
- Rate and review individual movies
- Automatically ranks movies based on rating
- Responsive UI with Bootstrap 5

---

## 📦 Installation

### 1. Clone the repository

```
git clone https://github.com/your-username/flask-movie-app.git
cd flask-movie-app
```
### 2. Install dependencies

#### on Mac:
```
pip install -r requirements.txt
```
#### on Windows:
```
python -m pip install -r requirements.txt
```
### 3. 🔐 Environment Variables
#### Create a .env file in your root directory and add the following:

- API_KEY_TMDB=your_tmdb_api_key_here
- SECRET_KEY_APP=your_flask_secret_key

#### Or export them in your shell:

- export API_KEY_TMDB=your_tmdb_api_key_here
- export SECRET_KEY_APP=your_flask_secret_key

## 🧪 Tech Stack
- Flask

- [Flask-WTF](https://flask-wtf.readthedocs.io/en/1.2.x/)

- [Flask-Bootstrap](https://bootstrap-flask.readthedocs.io/en/stable/)

- SQLAlchemy

- [WTForms](https://pypi.org/project/WTForms/)

- TMDb API

## 📁 Project Structure

[```templates/ ```](https://flask.palletsprojects.com/en/stable/tutorial/templates/)
- Contains Jinja-powered HTML templates rendered by Flask.

- index.html: Homepage listing all movies with rankings

- add.html: Form to input movie title, rating, review

- select.html: Displays movie search results from TMDb

- edit.html: Allows updating rating/review

- base.html: Base layout inherited by all other templates

[``` static/ ```](https://flask.palletsprojects.com/en/stable/tutorial/static/)
- Stores static files (CSS, JS, images).

- For example: static/css/styles.css holds your custom styles.

## 💡 Future Enhancements
- User authentication (e.g., Google or GitHub OAuth)

- Pagination and search for large movie libraries

- Docker support for easy deployment

- User-specific movie collections