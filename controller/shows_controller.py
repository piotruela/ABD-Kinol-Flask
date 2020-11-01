import datetime

from flask import render_template, Blueprint, request, redirect, url_for
from flask_login import login_required

from app import Session
from service import show_service, ticket_service, movie_service, room_service

shows = Blueprint('shows', __name__)


@shows.route('/shows')
@login_required
def get_shows():
    date_str = request.args.get('for_date') or datetime.datetime.now().date().__str__()
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    session = Session()
    shows_list = show_service.get_shows(date, session=session)
    for show in shows_list:
        show.left_tickets = ticket_service.count_left(show, session=session)
    return render_template('shows.html', shows=shows_list, for_date=date)


@shows.route('/shows/<show_id>')
@login_required
def get_show(show_id):
    session = Session()
    show = show_service.get_show(show_id, session)
    movies = movie_service.get_movies(session)
    rooms = room_service.get_rooms(session)
    return render_template('show.html', show=show, movies=movies, rooms=rooms)


@shows.route('/shows/create')
@login_required
def create_show():
    movies = movie_service.get_movies()
    rooms = room_service.get_rooms()
    return render_template('shows-create.html', movies=movies, rooms=rooms)


@shows.route('/shows/create', methods=['POST'])
@login_required
def create_show_post():
    movie_id = request.form.get('movie')
    room_id = request.form.get('room')
    date_time = datetime.datetime.strptime(request.form.get('date_time'), '%Y-%m-%d %H:%M')
    show = show_service.create(movie_id, room_id, date_time)
    return redirect(url_for('shows.get_show', show_id=show.id))


@shows.route('/shows/update/<show_id>', methods=['POST'])
@login_required
def update_show(show_id):
    movie_id = request.form.get('movie')
    room_id = request.form.get('room')
    date_time = datetime.datetime.strptime(request.form.get('date_time'), '%Y-%m-%d %H:%M')
    show = show_service.update(show_id, movie_id, room_id, date_time)
    return redirect(url_for('shows.get_show', show_id=show.id))


@shows.route('/shows/delete/<show_id>', methods=['POST'])
@login_required
def delete_show(show_id):
    show_service.delete(show_id)
    return redirect(url_for('shows.get_shows'))
