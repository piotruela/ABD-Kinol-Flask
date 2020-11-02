from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app import Base
from entity.movie import Movie
from entity.room import Room


class Show(Base):
    __tablename__ = 'show'

    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean)
    show_date = Column(DateTime)
    room_id = Column(Integer, ForeignKey('room.id'))
    movie_id = Column(Integer, ForeignKey('movie.id'))
    archived = Column(Boolean)

    room = relationship('Room', back_populates='shows')
    movie = relationship('Movie', back_populates='shows')


Movie.shows = relationship('Show', order_by=Show.id, back_populates='movie')
Room.shows = relationship('Show', order_by=Show.id, back_populates='room')
