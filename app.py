from flask import Flask
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from entity.base import Base
from entity.employee import Employee
from entity.movie import Movie
from entity.person import Person
from entity.room import Room
from entity.show import Show
from entity.sit import Sit
from entity.ticket import Ticket
from entity.ticket_number import TicketNumber

# ******
# Imports above from entity.* must be there to create database schema and register classes in sqlalchemy XD
# *****

app = Flask(__name__)


if __name__ == 'app':
    engine = create_engine('postgresql://kinol_user:kinol_password@localhost:5455/kinol', echo=True)

    app.config['SECRET_KEY'] = 'a2193hXC87g'
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)

    from controller.authentication_controller import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from controller.main_controller import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from controller.movies_controller import movies as movies_blueprint
    app.register_blueprint(movies_blueprint)
    from controller.shows_controller import shows as shows_blueprint
    app.register_blueprint(shows_blueprint)
    from controller.rooms_controller import rooms as rooms_blueprint
    app.register_blueprint(rooms_blueprint)
    from controller.employees_controller import employees as employees_blueprint
    app.register_blueprint(employees_blueprint)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Session().query(Person).filter_by(id=int(user_id)).first()

    app.run()


