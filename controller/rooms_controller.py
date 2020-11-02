from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_required

from app import Session
from entity.sit import Sit
from service import room_service, show_service, ticket_service, sit_service

rooms = Blueprint('rooms', __name__)


@rooms.route('/rooms')
@login_required
def get_rooms():
    rooms_list = room_service.get_rooms()
    return render_template('rooms.html', rooms=rooms_list)


@rooms.route('/rooms/<room_id>')
@login_required
def get_room(room_id):
    session = Session()
    room = room_service.get_room(room_id, session=session)
    upcoming_shows = show_service.get_upcoming_shows_by_room(room, session=session)
    sits = sit_service.get_sits_by_room(room, session=session)
    for show in upcoming_shows:
        show.left_tickets = ticket_service.count_left(show, session=session)
    return render_template('room.html', room=room, upcoming_shows=upcoming_shows, sits=sits)


@rooms.route('/rooms/create')
@login_required
def create_room():
    return render_template('rooms-create.html')


@rooms.route('/rooms/create', methods=['POST'])
@login_required
def create_room_post():
    number = request.form.get('number')
    rows = request.form.get('rows')
    columns = request.form.get('columns')
    sits = []
    for k, v in request.form.items():
        if k.startswith("sit-"):
            row_column = k.replace('sit-', '').split('-')
            sits.append(Sit(row=row_column[0], sit=row_column[1]))
    room = room_service.create(number, rows, columns, sits)
    return redirect(url_for('rooms.get_room', room_id=room.id))


@rooms.route('/rooms/archive_switch/<room_id>', methods=['POST'])
@login_required
def archive_room_switch(room_id):
    room_service.archive_switch(room_id)
    return redirect(url_for('rooms.get_room', room_id=room_id))
