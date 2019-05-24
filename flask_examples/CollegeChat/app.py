from flask import Flask, g, render_template, request, redirect, url_for, abort, flash, get_flashed_messages
import os, sqlite3
from flask_examples.CollegeChat import cc_classes

# Instantiate a Flask webapp object
app = Flask(__name__)

# Configure the app object
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'CC.db'), # Set the path to the database to be used with the webapp
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

@app.route('/chatroom/<chatroomID>/view')
def view_chatroom(chatroomID):

    chatroom = cc_classes.Chatroom(chatroomID)

    return render_template('chatroom.html', cr=chatroom)


@app.route('/chatroom/<chatroomID>/messages/add', methods=['post'])
def add_message_to_chatroom(chatroomID):

    message_text = request.form['new_message_text']
    ip = request.remote_addr
    ua = str(request.user_agent)

    cr = cc_classes.Chatroom(chatroomID)

    cr.add_message(message_text, cc_classes.User(1), ip, ua)

    return redirect(url_for('view_chatroom', chatroomID=chatroomID))




@app.route('/messages/view/<id>')
def view_message(id):
    m = cc_classes.Message(id)
    return render_template('view_message.html', message=m)


@app.route('/users/add', methods=['GET', 'POST'])
def register_new_user():

    if request.method == "GET":

        return render_template('new_user.html', flash_messages=get_flashed_messages())

    else:

        # Check passwords match

        if request.form['password'] != request.form['confirm_password']:
            flash("Passwords do not match!", "errors")
            flash("test")
            return redirect(url_for('register_new_user'))

        try:

            new_user = cc_classes.User.add_to_db(request.form['username'], request.form['email'], request.form['password'], 'StandardUser')

            return 'User created! ID: {}'.format(new_user.id)

        except sqlite3.IntegrityError as e:

            flash(str(e), "errors")
            return redirect(url_for('register_new_user'))

# TEST ROUTES
@app.route('/tests/users/<id>')
def tests_user_id(id):
    u = cc_classes.User(id)
    return "User object - Username: {}, email: {}, joined: {}".format(u.username, u.email, u.joined)

@app.route('/tests/messages/<int:id>')
def tests_messages_id(id):

    try:
        m = cc_classes.Message(id)
        return "Message ID: {}, Contents: {}, Sender: {}, Message sent: {}".format(m.id, m.contents, m.sender.username, m.ts)
    except cc_classes.MessageNotFoundError:
        return "Message not found", 404

@app.route('/tests/messages/add')
def tests_messages_add():
    m = cc_classes.Message.add_to_db("A new message added by the test route /tests/messages/add", 1, 1, request.remote_addr, "No UA: TEST METHOD")
    return "Message ID: {}, Contents: {}, Sender: {}, Message sent: {}".format(m.id, m.contents, m.sender.username, m.ts)

@app.route('/tests/chatrooms/add/<name>')
def tests_chatroom_add(name):

    cr = cc_classes.Chatroom.add_to_db(name, False, cc_classes.User(1))

    return "Chatroom added! ID: {}, Name: {}, Owners: {}".format(cr.id, cr.name, cr.owners)

# When this script is run directly by the Python interpreter, do the following...
if __name__ == '__main__':
    # Run the webapp in Debug mode (no need to restart when changes are made and set host to broadcast to allow
    # connections from other devices (i.e. not just localhost)
    app.run(debug=True, host="0.0.0.0")


