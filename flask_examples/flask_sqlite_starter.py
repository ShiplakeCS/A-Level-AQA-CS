from flask import Flask, g, render_template
import os
import sqlite3

# Instantiate a Flask webapp object
app = Flask(__name__)

# Configure the app object
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'sqlite_db.db'), # Set the path to the database to be used with the webapp
    SECRET_KEY='123456', # Define a secret key that is used for encrypting session cookies
))


def get_db():

    """
    Returns a connection to the database from the currently running Flask thread, as stored in the global variable
    'g'. This is used whenever we need to access the database to query it for data or insert/update data.
    """
    if not hasattr(g, 'db'):
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row  # Specify a dictionary-like Row object format for each query result
    return g.db


@app.teardown_appcontext
def close_db(error):
    """
    Closes the connection to the database for this application thread. Called automatically when the app closes.
    """
    if hasattr(g, 'db'):
       g.db.close()


# Define a default app route to run when a user vists the webapp's root URI ('/')
@app.route('/')
def hello_world():
    return '<h1 style="color:red">Hello World!</h1>'


# Define an app route that demonstrates how to pass dynamic URI paths as variables
@app.route('/hello/<user>')
def say_hello(user):
    return '<h1 style="color:red">Hello <span style="color:blue">{}</span>!</h1>'.format(user)


# When this script is run directly by the Python interpreter, do the following...
if __name__ == '__main__':
    # Run the webapp in Debug mode (no need to restart when changes are made and set host to broadcast to allow
    # connections from other devices (i.e. not just localhost)
    app.run(debug=True, host="0.0.0.0")
