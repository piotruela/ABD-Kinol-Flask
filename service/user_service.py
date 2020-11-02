from werkzeug.security import check_password_hash

from app import Session
from entity.person import Person


def authenticate(email: str, password: str) -> bool:
    session = Session()
    user = session.query(Person).filter_by(mail=email).first()
    return user if user and check_password_hash(user.password, password) and user.person_type == 'EMPLOYEE' else None
