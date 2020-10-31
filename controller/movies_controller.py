from flask import render_template, Blueprint
from flask_login import login_required

from service import movie_service

movies = Blueprint('movies', __name__)


@login_required
@movies.route('/movies')
def get_movies():
    movies_list = movie_service.get_movies()
    return render_template('movies.html', movies=movies_list)
