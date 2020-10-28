import os

from flask import Flask

from database import db
from views.person import people


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = bool(int(os.environ.get('DEBUG', False)))

    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////data/people.db3"
    db.init_app(app)
    app.register_blueprint(people, url_prefix='/people')
    return app


def setup_database(app):
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    from pprint import pprint
    app = create_app()
    if not os.path.isfile('/data/people.db3'):
        setup_database(app)

    pprint(app.config)
    app.run(
        host='0.0.0.0',
        debug=app.config['DEBUG']
    )
