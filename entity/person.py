from flask_login import UserMixin
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from entity.base import Base


class Person(UserMixin, Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    mail = Column(String, unique=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    person_type = Column(String)
    employee = relationship("Employee", uselist=False, back_populates="person")
