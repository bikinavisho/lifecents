from flask import Flask
import flask

app = Flask(__name__)


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
