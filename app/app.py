import os

from flask import Flask


app = Flask(__name__)


@app.route('/hello/<string:name>', methods=['GET'])
def hello(name):
    return f'Hello {name}'


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=os.environ.get('DEBUG', False)
    )
