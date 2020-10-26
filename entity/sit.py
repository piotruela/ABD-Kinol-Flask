from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app import Base
from entity.room import Room


class Sit(Base):
    __tablename__ = 'sit'

    id = Column(Integer, primary_key=True)
    row = Column(Integer)
    sit = Column(Integer)
    room_id = Column(Integer, ForeignKey('room.id'))

    room = relationship('Room', back_populates='sits')


Room.sits = relationship('Sit', order_by=Sit.id, back_populates='room')
