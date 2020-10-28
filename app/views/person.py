"""
This file contains the definition of the Person object
"""
import json

from flask import request
from flask.blueprints import Blueprint

from database import db


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
    first_name = db.Column(db.String(255), nullable=False)
    middle_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    version = db.Column(db.Integer, nullable=False)

    deleted = db.Column(db.Boolean, nullable=False)

    def as_dict(self):
        return {
            col.name: getattr(self, col.name)
            for col in self.__table__.columns
        }


@people.route('')
def get_people():
    """
    Returns the most recent version for each person
    """
    people_list = [
        row._asdict()
        for row in db.session.query(
            PersonVersion.person_id,
            PersonVersion.first_name,
            PersonVersion.middle_name,
            PersonVersion.last_name,
            PersonVersion.email,
            PersonVersion.age,
            PersonVersion.version,
            PersonVersion.deleted,
            db.func.max(PersonVersion.version)
        ).group_by(
            PersonVersion.person_id,
            PersonVersion.first_name,
        ).order_by(
            PersonVersion.person_id
        ).all()
    ]

    return json.dumps([
        dict(filter(lambda x: x[0] != 'deleted', row.items()))
        for row in people_list
        if row.get('deleted') is False
    ])


@people.route('/<string:_id>')
def get_person(_id):
    """
    Returns a single version of a single person.

    The version number is optional and included
    in the query string as "version"
    """
    if version := request.args.get('version'):
        try:
            version = int(version)
        except ValueError:
            return {"message": "Bad query param"}, 400
        ret = PersonVersion.query.filter(
            PersonVersion.person_id == _id,
            PersonVersion.version == version
        ).first_or_404()
    else:
        ret = PersonVersion.query.filter(
            PersonVersion.person_id == _id,
        ).order_by(
            PersonVersion.version.desc()
        ).first_or_404()

    if ret.deleted:
        return {"deleted": True}, 404
    del(ret.deleted)

    return ret.as_dict()


@people.route('/add', methods=['POST'])
def add_person():
    json_args = request.get_json()
    if not json_args:
        return {"message": "Bad request"}, 400

    # Create the Person record first
    # TODO: Wrap both cretes in a transaction
    new_person = Person()
    db.session.add(new_person)
    db.session.commit()

    # Now that we have an ID we can make the first version
    first_version = PersonVersion(
        person_id=new_person.id,
        first_name=json_args["first_name"],
        middle_name=json_args.get('middle_name'),
        last_name=json_args["last_name"],
        email=json_args["email"],
        age=json_args["age"],
        version=1,
        deleted=False
    )
    db.session.add(first_version)
    db.session.commit()

    del(first_version.deleted)

    return first_version.as_dict()


@people.route('/update/<int:_id>', methods=['PATCH'])
def update_person(_id):
    """
    Adds a new version of a person with potentially different
    values.
    """
    json_args = request.get_json()
    if not json_args:
        return {"message": "Bad request"}, 400

    # Get the existing record to base the update on
    previous_version = PersonVersion.query.filter(
        PersonVersion.person_id == _id
    ).order_by(
        PersonVersion.version.desc()
    ).first_or_404()

    if previous_version.deleted:
        return {"deleted": True}, 404

    # Increment the version
    new_version_number = previous_version.version + 1

    # Copy the object
    new_version = PersonVersion(
        **previous_version.as_dict()
    )

    for col, val in json_args.items():
        setattr(new_version, col, val)

    new_version.version = new_version_number
    del(new_version.id)

    db.session.add(new_version)
    db.session.commit()

    return new_version.as_dict()


@people.route('/delete/<int:_id>', methods=['DELETE'])
def delete_person(_id):
    """
    Adds a new version with NULL values for the person
    """
    # TODO: Wrap this logic in one function for update/delete
    # Get the existing record to base the update on
    previous_version = PersonVersion.query.filter(
        PersonVersion.person_id == _id
    ).order_by(
        PersonVersion.version.desc()
    ).first_or_404()

    if previous_version.deleted:
        return {
            "person_id": previous_version.person_id,
            "deleted": previous_version.deleted
        }

    # Increment the version
    new_version_number = previous_version.version + 1

    # Copy the object
    new_version = PersonVersion(
        **previous_version.as_dict()
    )

    new_version.version = new_version_number
    new_version.deleted = True
    del(new_version.id)

    db.session.add(new_version)
    db.session.commit()

    return {
        "person_id": new_version.person_id,
        "deleted": new_version.deleted
    }
