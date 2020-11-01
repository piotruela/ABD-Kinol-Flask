from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_required

from app import Session
from service import room_service, show_service, ticket_service, sit_service

rooms = Blueprint('rooms', __name__)


@rooms.route('/rooms')
@login_required
def get_rooms():
    rooms_list = room_service.get_rooms()
    return render_template('rooms.html', rooms=rooms_list)


# todo - dodac jeszcze siatke z siedzeniami i dodawanie siedzen
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


# todo - siatka z siedzeniami i dodawanie siedzen
@rooms.route('/rooms/create')
@login_required
def create_room():
    return render_template('rooms-create.html')


# todo- siatka z siedzeniami i dodawanie siedzen
@rooms.route('/rooms/create', methods=['POST'])
@login_required
def create_room_post():
    number = request.form.get('number')
    room = room_service.create(number)
    return redirect(url_for('rooms.get_room', room_id=room.id))


# todo- siatka z siedzeniami i dodawanie siedzen
@rooms.route('/rooms/update/<room_id>', methods=['POST'])
@login_required
def update_room(room_id):
    number = request.form.get('number')
    room = room_service.update(room_id, number)
    return redirect(url_for('rooms.get_room', room_id=room.id))


@rooms.route('/rooms/delete/<room_id>', methods=['POST'])
@login_required
def delete_room(room_id):
    room_service.delete(room_id)
    return redirect(url_for('rooms.get_rooms'))
