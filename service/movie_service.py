from typing import List

from app import Session
from entity.movie import Movie


def get_movies() -> List[Movie]:
    session = Session()
    return session.query(Movie).all()


def create(title, minimum_age, genre, length_minutes, description):
    session = Session()
    movie = Movie(title=title, minimum_age=minimum_age, genre=genre, length_minutes=length_minutes,
                  describe=description)
    session.add(movie)
    session.commit()
    return movie


def get_movie(movie_id):
    session = Session()
    return session.query(Movie).filter_by(id=movie_id).first()


def delete(movie_id):
    session = Session()
    movie = session.query(Movie).filter_by(id=movie_id).first()
    session.delete(movie)
    session.commit()


def update(movie_id, title, minimum_age, genre, length_minutes, description):
    session = Session()
    movie = session.query(Movie).filter_by(id=movie_id).first()
    movie.title = title
    movie.minimum_age = minimum_age
    movie.genre = genre
    movie.length_minutes = length_minutes
    movie.describe = description
    session.commit()
    return movie
