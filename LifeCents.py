from flask import Flask
import flask
import flask_sqlalchemy
import dataBaser
import base64, os

app = Flask(__name__)
app.config.from_pyfile('settings.py')
db = flask_sqlalchemy.SQLAlchemy(app)


@app.before_request
def setup_user():
    """
    Figure out if we have an authorized user, and look them up.
    This runs for every request, so we don't have to duplicate code.
    """
    if 'auth_user' in flask.session:
        user = dataBaser.User.query.get(flask.session['auth_user'])
        if user is None:
            # old bad cookie, no good
            del flask.session['auth_user']
        # save the user in `flask.g`, which is a set of globals for this request
        flask.g.user = user


@app.before_request
def setup_csrf():
    # make a cross-site request forgery preventing token
    if 'csrf_token' not in flask.session:
        flask.session['csrf_token'] = base64.b64encode(os.urandom(32)).decode('ascii')


# This signifies that when you navigate to the URL / on our homepage (lcents.com/) it will run this function
@app.route('/')
def render_homepage():
    # This signifies that at the end of the function it will render the index.html template.
    # We can add additional arguments to it if we want to pass data
        # Ex: flask.render_template('index.html', var1, var2)
        #       and in the html file you would put {{ var1 }} to print its value
    return flask.render_template('index.html')


# This runs the application which is our website
if __name__ == '__main__':
    app.run()
