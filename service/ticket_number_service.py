from entity.ticket_number import TicketNumber


def get_and_inc_next_number(session) -> TicketNumber:
    ticket_number = session.query(TicketNumber).with_for_update().first()
    ticket_number.number += 1
    return ticket_number
