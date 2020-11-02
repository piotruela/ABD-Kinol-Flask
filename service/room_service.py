from app import Session
from entity.room import Room


def get_rooms(session=Session()):
    return session.query(Room).filter_by(archived=False).all()


def get_room(room_id, session=Session()):
    return session.query(Room).filter_by(id=room_id).first()


def create(number, rows, columns, sits):
    session = Session()
    room = Room(number=number, capacity=len(sits), rows=rows, columns=columns, archived=False)
    room.sits = sits
    session.add(room)
    session.commit()
    return room


def archive_switch(room_id):
    session = Session()
    room = get_room(room_id, session)
    room.archived = not room.archived
    session.commit()
