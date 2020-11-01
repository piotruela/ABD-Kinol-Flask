from datetime import datetime
from typing import List

from sqlalchemy import and_

from app import Session
from entity.show import Show
from service import movie_service, room_service


def get_shows(date: datetime.date) -> List[Show]:
    session = Session()
    date_time_start = datetime.combine(date, datetime.min.time())
    date_time_end = datetime.combine(date, datetime.max.time())
    return session.query(Show).filter(and_(Show.show_date.between(date_time_start, date_time_end))).all()


def get_show(show_id, session=Session()):
    return session.query(Show).filter_by(id=show_id).first()


def create(movie_id, room_id, date_time):
    session = Session()
    movie = movie_service.get_movie(movie_id, session=session)
    room = room_service.get_room(room_id, session=session)
    show = Show(is_active=True, show_date=date_time, room=room, movie=movie)
    session.add(show)
    session.commit()
    return show


def delete(show_id):
    session = Session()
    show = session.query(Show).filter_by(id=show_id).first()
    session.delete(show)
    session.commit()


def update(show_id, movie_id, room_id, date_time):
    session = Session()
    show = get_show(show_id, session)
    show.show_date = date_time
    show.room = room_service.get_room(room_id, session)
    show.movie = movie_service.get_movie(movie_id, session)
    session.commit()
    return show
