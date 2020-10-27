import os
import json

from flask import Flask
from sqlalchemy import create_engine, orm

from people import Base, People


app = Flask(__name__)


@app.route('/hello/<string:name>', methods=['GET'])
def hello(name):
    return f'Hello {name}'


@app.route('/people', methods=['GET'])
def get_people():
    return json.dumps([
       i.as_dict()
       for i in app.sesh.query(People).all()
    ])


@app.route('/people', methods=['POST'])
def add_person(**kwargs):
    new_person = People(**kwargs)
    app.sesh.add(new_person)
    app.sesh.commit()

    return "OK"


if __name__ == '__main__':
    print(People)

    engine = create_engine('sqlite:////data/people.db3')
    Base.metadata.create_all(engine)

    Base.metadata.bind = engine

    DBsession = orm.sessionmaker()
    DBsession.bind = engine
    session = DBsession()

    app.sesh = session

    app.run(
        host='0.0.0.0',
        debug=os.environ.get('DEBUG', False)
    )
