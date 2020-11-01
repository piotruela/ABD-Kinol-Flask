from app import Session
from entity.room import Room


def get_rooms(session=Session()):
    return session.query(Room).all()


def get_room(room_id, session=Session()):
    return session.query(Room).filter_by(id=room_id).first()
