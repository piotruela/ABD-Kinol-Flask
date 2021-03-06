from app import Session
from entity.sit import Sit


def get_sits_by_room(room, session=Session()):
    return session.query(Sit).filter_by(room_id=room.id).all()


def get_sit(sit_id, session=Session()):
    return session.query(Sit).filter_by(id=sit_id).first()
