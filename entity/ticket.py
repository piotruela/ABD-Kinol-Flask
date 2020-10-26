from sqlalchemy import Integer, Column, String, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship

from app import Base
from entity.employee import Employee
from entity.show import Show
from entity.sit import Sit


class Ticket(Base):
    __tablename__ = 'ticket'

    id = Column(Integer, primary_key=True)
    was_paid = Column(Boolean)
    booking_date = Column(DateTime)
    discount_code = Column(String)
    show_id = Column(Integer, ForeignKey('show.id'))
    sit_id = Column(Integer, ForeignKey('sit.id'))
    employee_id = Column(Integer, ForeignKey('employee.id'))
    price = Column(Float)
    ticket_number = Column(Integer)

    employee = relationship('Employee', back_populates='tickets')
    sit = relationship('Sit', back_populates='tickets')
    show = relationship('Show', back_populates='tickets')


Employee.tickets = relationship('Ticket', order_by=Ticket.id, back_populates='employee')
Sit.tickets = relationship('Ticket', order_by=Ticket.id, back_populates='sit')
Show.tickets = relationship('Ticket', order_by=Ticket.id, back_populates='show')
