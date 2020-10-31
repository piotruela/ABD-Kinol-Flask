from typing import List

from app import Session
from entity.movie import Movie


def get_movies() -> List[Movie]:
    session = Session()
    return session.query(Movie).all()
