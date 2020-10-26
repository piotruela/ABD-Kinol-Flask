from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from entity import *
from entity.base import Base
from entity.movie import Movie

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == 'app':
    engine = create_engine('postgresql://kinol_user:kinol_password@localhost:5455/kinol', echo=True)

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    app.run()
