"""
This file contains the definition of the Person object
"""
import json
from database import db
from flask.blueprints import Blueprint


people = Blueprint('people', __name__)


class Person(db.Model):
    """
    This table's rows each represent a person
    """

    id = db.Column(db.Integer, primary_key=True)

    versions = db.relationship(
        'PersonVersion',
        backref='person',
        lazy=True
    )

    def as_dict(self):
        return {
            col.name: getattr(self, col.name)
            for col in self.__table__.columns
        }


class PersonVersion(db.Model):
    """
    This table's rows each represent a versioned, temporal
    representation of a person.
    """
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(
        db.Integer,
        db.ForeignKey('person.id'),
        nullable=False
    )

    first_name = db.Column(db.String(255))
    middle_name = db.Column(db.String(255))
    last_name = db.Column(db.String(2355))
    email = db.Column(db.String(255))
    age = db.Column(db.Integer)

    version = db.Column(db.Integer, nullable=False)


@people.route('')
def get_people():
    return json.dumps([
        row._asdict()
        for row in db.session.query(
            PersonVersion.person_id,
            PersonVersion.first_name,
            PersonVersion.version,
            db.func.max(PersonVersion.version)
        ).group_by(
            PersonVersion.person_id,
            PersonVersion.first_name,
            PersonVersion.version
        ).order_by(
            PersonVersion.person_id
        ).all()
    ])


@people.route('/<string:_id>')
def get_person(_id):
    return PersonVersion.query.filter(
        PersonVersion.person_id == _id
    ).order_by(
        PersonVersion.version.desc()
    ).first_or_404()


@people.route('/add', methods=['POST'])
def add_person():
    # Create the Person record first
    new_person = Person()
    db.session.add(new_person)
    db.session.commit()

    # Now that we have an ID we can make the first version
    first_version = PersonVersion(
        person_id=new_person.id,
        first_name='Bob',
        version=1
    )
    db.session.add(first_version)
    db.session.commit()

    return new_person.as_dict()
