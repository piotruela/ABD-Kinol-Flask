from sqlalchemy import Integer, Column

from app import Base


class TicketNumber(Base):
    __tablename__ = 'ticket_number'

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
