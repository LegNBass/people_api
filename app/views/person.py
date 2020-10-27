"""
This file contains the definition of the Person object
"""
import json
from database import db
from flask.blueprints import Blueprint

people = Blueprint('people', __name__)


class Person(db.Model):
    """
    ORM definition of the people table
    """

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    middle_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(2355))
    email = db.Column(db.String(255))
    age = db.Column(db.Integer)
    version = db.Column(db.Integer)

    def as_dict(self):
        return {
            col.name: getattr(self, col.name)
            for col in self.__table__.columns
        }


@people.route('/')
def get_people():
    return json.dumps(
        Person.query.all()
    )
