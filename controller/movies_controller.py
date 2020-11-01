from flask import render_template, Blueprint, request, redirect, url_for
from flask_login import login_required

from service import movie_service

movies = Blueprint('movies', __name__)


@movies.route('/movies')
@login_required
def get_movies():
    movies_list = movie_service.get_movies()
    return render_template('movies.html', movies=movies_list)

#todo powinna byc jeszcze lista seansow dotyczaca filmu
@movies.route('/movies/<movie_id>')
@login_required
def get_movie(movie_id):
    movie = movie_service.get_movie(movie_id)
    return render_template('movie.html', movie=movie)


@movies.route('/movies/create')
@login_required
def create_movie():
    return render_template('movies-create.html')


@movies.route('/movies/create', methods=['POST'])
@login_required
def create_movie_post():
    title = request.form.get('title')
    minimum_age = request.form.get('minimum_age')
    genre = request.form.get('genre')
    length_minutes = request.form.get('length_minutes')
    description = request.form.get('description')
    movie = movie_service.create(title, minimum_age, genre, length_minutes, description)
    return redirect(url_for('movies.get_movie', movie_id=movie.id))


@movies.route('/movies/update/<movie_id>', methods=['POST'])
@login_required
def update_movie(movie_id):
    title = request.form.get('title')
    minimum_age = request.form.get('minimum_age')
    genre = request.form.get('genre')
    length_minutes = request.form.get('length_minutes')
    description = request.form.get('description')
    movie = movie_service.update(movie_id, title, minimum_age, genre, length_minutes, description)
    return redirect(url_for('movies.get_movie', movie_id=movie.id))


@movies.route('/movies/delete/<movie_id>', methods=['POST'])
@login_required
def delete_movie(movie_id):
    movie_service.delete(movie_id)
    return redirect(url_for('movies.get_movies'))
