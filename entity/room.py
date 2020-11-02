from sqlalchemy import Column, Integer, Boolean

from app import Base


class Room(Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True)
    capacity = Column(Integer)
    number = Column(Integer)
    rows = Column(Integer)
    columns = Column(Integer)
    archived = Column(Boolean)
