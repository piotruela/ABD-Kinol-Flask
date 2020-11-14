import datetime

from flask import Blueprint, request
from sqlalchemy import and_
from sqlalchemy.sql import text

from app import Session
from entity.show import Show
from entity.ticket import Ticket
from entity.ticket_number import TicketNumber

tasks = Blueprint('tasks', __name__)


# Task 1:
# Wstaw do tabeli ticket kolejny bilet pobierając z tabeli ticket_number kolejny numer i zwiększ wartość w tabeli ticket_number o 1.
# Jeżeli ticket_number jest wielokrotnością 100 to wpisz kod HAPPY100 w discount_code i obniż cenę o 20%.
# Jeżeli sala jest zapełniona w ponad 90% procentach to obniż cenę o dodatkowe 10% i zmień discount_code na  (HAPPY100+10).

@tasks.route('/tasks/1')
def compute_task_1():
    desired_show_id = 5
    desired_sit_id = request.args.get('sit_id') or 4
    employee_id = 1

    start = datetime.datetime.now()
    # task_1_orm(desired_show_id, desired_sit_id, employee_id)
    task_1_sql(desired_show_id, desired_sit_id, employee_id)
    end = datetime.datetime.now()
    execution_in_millis = (end - start).total_seconds() * 1000
    return 'task1done ' + str(execution_in_millis)


# Wyszukaj sale, w których średnie zagęszczenie na seansach grupując po gatunkach filmów i pór seansów
# (rano, okolice południa, południe, wieczór/noc) było większe niż x%.
# todo orm
@tasks.route('/tasks/2')
def compute_task_2():
    zageszczenie = request.args.get('zageszczenie') or 10

    start = datetime.datetime.now()
    wyniki = task_2_sql(zageszczenie)
    end = datetime.datetime.now()
    execution_in_millis = (end - start).total_seconds() * 1000
    return 'task2done ' + str(execution_in_millis) + 'ms ' + str(wyniki)


def task_1_orm(desired_show_id, desired_sit_id, employee_id):
    base_price = 20.00
    session = Session()
    ticket_number = session.query(TicketNumber).with_for_update().first()
    ticket_number.number = ticket_number.number + 1
    if session.query(Ticket).filter(
            and_(Ticket.show_id == desired_show_id, Ticket.sit_id == desired_sit_id)).count() > 0:
        raise Exception("Sit {} for show {} is busy".format(desired_sit_id, desired_show_id))
    discount_code = ''
    discount_percentage = 0
    show = session.query(Show).filter_by(id=desired_show_id).first()
    if ticket_number.number % 100 == 0:
        discount_percentage = 20
        discount_code = 'HAPPY_100'
        sits_taken = session.query(Ticket).filter_by(show_id=desired_show_id).count()
        available_sits = show.room.capacity
        if sits_taken * 1.0 / available_sits > 0.9:
            discount_code += '+10'
            discount_percentage += 10
    final_price = base_price - base_price * discount_percentage / 100
    ticket = Ticket(was_paid=True, booking_date=datetime.datetime.now(), discount_code=discount_code, price=final_price,
                    sit_id=desired_sit_id, show=show, employee_id=employee_id, ticket_number=ticket_number.number)
    session.add(ticket)
    session.commit()


def task_1_sql(desired_show_id, desired_sit_id, employee_id):
    base_price = 20.00

    session = Session()
    number = session.execute("select ticket_number.number from ticket_number for update limit 1").fetchall()
    number = number[0][0] + 1
    stmt = text("update ticket_number set number = :ticket_number")
    stmt = stmt.bindparams(ticket_number=number)
    session.execute(stmt)

    stmt = text("select count(*) from ticket where ticket.show_id = :show_id and ticket.sit_id = :sit_id")
    stmt = stmt.bindparams(show_id=desired_show_id, sit_id=desired_sit_id)
    if session.execute(stmt).fetchall()[0][0] > 0:
        raise Exception("Sit {} for show {} is busy".format(desired_sit_id, desired_show_id))

    discount_code = ''
    discount_percentage = 0
    stmt = text("select show.id, room.capacity from show join room on room.id = show.room_id where show.id = :show_id")
    stmt = stmt.bindparams(show_id=desired_show_id)

    show = session.execute(stmt).fetchall()

    if number % 100 == 0:
        discount_percentage = 20
        discount_code = 'HAPPY_100'
        stmt = text("select count(*) from ticket where ticket.show_id=:show_id")
        stmt = stmt.bindparams(show_id=desired_show_id)
        sits_taken = session.execute(stmt).fetchall()[0][0]
        available_sits = show[0][1]
        if sits_taken * 1.0 / available_sits > 0.9:
            discount_code += '+10'
            discount_percentage += 10
    final_price = base_price - base_price * discount_percentage / 100
    stmt = text(
        "insert into ticket(was_paid, booking_date, discount_code, price, sit_id, show_id, employee_id, ticket_number) "
        "values (:was_paid, :booking_date, :discount_code, :price, :sit_id, :show_id, :employee_id, :ticket_number)")
    stmt = stmt.bindparams(was_paid=True, booking_date=datetime.datetime.now(), discount_code=discount_code,
                           price=final_price,
                           sit_id=desired_sit_id, show_id=show[0][0], employee_id=employee_id, ticket_number=number)

    session.execute(stmt)
    session.commit()


def task_2_sql(zageszczenie):
    session = Session()
    stmt = text(
        "select * from (select count(ticket) * 100.0 / (r.capacity * count(distinct s.id)) as zageszczenie,r.id,m.genre, "
        "case when ((extract(hour from show_date)) > 5 and (extract(hour from show_date)) <= 10) then 'rano'"
        "when ((extract(hour from show_date)) > 10 and (extract(hour from show_date)) <= 12) then 'poludnie'"
        "when ((extract(hour from show_date)) > 12 and (extract(hour from show_date)) <= 18) then 'po poludniu'"
        "when ((extract(hour from show_date)) > 18 and (extract(hour from show_date)) <= 20) then 'wieczor'"
        "else 'noc' END as pora "
        "from ticket "
        "left join show s on ticket.show_id = s.id "
        "left join room r on s.room_id = r.id "
        "left join movie m on s.movie_id = m.id "
        "group by r.id, m.genre, pora) as task2 "
        "where zageszczenie > :zageszczenie")
    stmt = stmt.bindparams(zageszczenie=zageszczenie)
    result = session.execute(stmt).fetchall()
    wynik = []
    for row in result:
        wynik.append((row[0], row[1], row[2], row[3]))
    return wynik