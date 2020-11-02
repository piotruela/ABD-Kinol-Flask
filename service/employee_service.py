from app import Session
from entity.employee import Employee


def get_employee(employee_id: int, session=Session()) -> Employee:
    return session.query(Employee).filter_by(id=employee_id).first()


def get_employee_by_person(profile_id, session=Session()):
    return session.query(Employee).filter_by(person_id=profile_id).first()
