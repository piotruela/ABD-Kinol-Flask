from app import Session
from entity.ticket import Ticket


def count_reserved(show, session):
    return session.query(Ticket).filter_by(show_id=show.id).count()


def count_left(show, session=Session()) -> int:
    reserved = count_reserved(show, session)
    return show.room.capacity - reserved
