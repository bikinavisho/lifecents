import flask
import flask_sqlalchemy
import os
from flask_socketio import SocketIO

app = flask.Flask(__name__)
app.config.from_pyfile('settings.py')
app.config.from_object(os.environ['SECRET_KEY'])
db = flask_sqlalchemy.SQLAlchemy(app)
socket_io = SocketIO(app)
