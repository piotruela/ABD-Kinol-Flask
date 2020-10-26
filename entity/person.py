from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from entity.base import Base


class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    employee = relationship("Employee", uselist=False, back_populates="person")
