from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from entity.base import Base


class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True)
    address = Column(String)
    is_hired = Column(Boolean)
    phone_number = Column(String)
    pesel = Column(String)
    employee_type = Column(String)
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship("Person", back_populates="employee")
