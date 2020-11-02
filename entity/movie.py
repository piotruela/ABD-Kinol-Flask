from sqlalchemy import Column, Integer, String, Boolean

from app import Base


class Movie(Base):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    length_minutes = Column(Integer)
    genre = Column(String)
    minimum_age = Column(Integer)
    describe = Column(String)
    title = Column(String)
    archived = Column(Boolean)
