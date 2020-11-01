from app import Session
from entity.room import Room


def get_rooms(session=Session()):
    return session.query(Room).all()


def get_room(room_id, session=Session()):
    return session.query(Room).filter_by(id=room_id).first()


def create(number):
    session = Session()
    room = Room(number=number, capacity=15)
    session.add(room)
    session.commit()
    return room


def update(room_id, number):
    session = Session()
    room = get_room(room_id, session)
    room.number = number
    session.commit()
    return room


def delete(room_id):
    session = Session()
    room = get_room(room_id, session)
    session.delete(room)
    session.commit()
