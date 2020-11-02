from app import Session
from entity.ticket import Ticket
from service import show_service, sit_service, employee_service, ticket_number_service


def count_reserved(show, session):
    return session.query(Ticket).filter_by(show_id=show.id).count()


def count_left(show, session=Session()) -> int:
    reserved = count_reserved(show, session)
    return show.room.capacity - reserved


def create(show_id, sit_id, logged_user_id, was_paid, booking_date, discount_code, price):
    session = Session()
    show = show_service.get_show(show_id, session=session)
    sit = sit_service.get_sit(sit_id, session=session)
    employee = employee_service.get_employee_by_person(logged_user_id, session=session)
    number = ticket_number_service.get_and_inc_next_number(session)
    ticket = Ticket(was_paid=was_paid, booking_date=booking_date, discount_code=discount_code, price=price,
                    sit=sit, show=show, employee=employee, ticket_number=number.number)
    session.add(ticket)
    session.commit()
    return ticket


def get_ticket(ticket_id, session=Session()):
    return session.query(Ticket).filter_by(id=ticket_id).first()


def update(ticket_id, was_paid, discount_code, price):
    session = Session()
    ticket = get_ticket(ticket_id, session)
    ticket.was_paid = was_paid
    ticket.discount_code = discount_code
    ticket.price = price
    session.commit()
    return ticket


def delete(ticket, session=Session()):
    session.delete(ticket)
    session.commit()
