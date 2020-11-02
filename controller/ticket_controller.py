import datetime

from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_required

from app import Session
from service import show_service, ticket_service, sit_service

tickets = Blueprint('tickets', __name__)


@tickets.route('/tickets/create')
@login_required
def create_ticket():
    show_id = request.args.get('show_id')
    sit_id = request.args.get('sit_id')
    show = show_service.get_show(show_id)
    sit = sit_service.get_sit(sit_id)
    return render_template('tickets-create.html', show=show, sit=sit)


@tickets.route('/tickets/<ticket_id>')
@login_required
def get_ticket(ticket_id):
    ticket = ticket_service.get_ticket(ticket_id)
    return render_template('ticket.html', ticket=ticket)


@tickets.route('/tickets', methods=['POST'])
@login_required
def create_ticket_post():
    show_id = request.form.get('show_id')
    sit_id = request.form.get('sit_id')
    logged_user_id = request.form.get('logged_user_id')
    was_paid = True if request.form.get('was_paid') == 'True' else False
    booking_date = datetime.datetime.now()
    discount_code = request.form.get('discount_code')
    price = request.form.get('price')
    ticket = ticket_service.create(show_id, sit_id, logged_user_id, was_paid, booking_date, discount_code, price)
    return redirect(url_for('tickets.get_ticket', ticket_id=ticket.id))


@tickets.route('/tickets/update/<ticket_id>', methods=['POST'])
@login_required
def update_ticket(ticket_id):
    was_paid = True if request.form.get('was_paid') == 'True' else False
    discount_code = request.form.get('discount_code')
    price = request.form.get('price')
    ticket_service.update(ticket_id, was_paid, discount_code, price)
    return redirect(url_for('tickets.get_ticket', ticket_id=ticket_id))


@tickets.route('/tickets/delete/<ticket_id>', methods=['POST'])
@login_required
def delete_ticket(ticket_id):
    session = Session()
    ticket = ticket_service.get_ticket(ticket_id, session=session)
    show_id = ticket.show_id
    ticket_service.delete(ticket, session=session)
    return redirect(url_for('shows.get_show', show_id=show_id))
