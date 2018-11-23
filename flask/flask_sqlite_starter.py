from flask import Flask, g, render_template
import os
import sqlite3

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'sqlite_db.db'),
    SECRET_KEY='123456',
))


def get_db():
    if not hasattr(g, 'db'):
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
   if hasattr(g, 'db'):
       g.db.close()


@app.route('/')
def hello_world():
    return '<h1 style="color:red">Hello World!</h1>'


@app.route('/hello/<user>')
def say_hello(user):
    return '<h1 style="color:red">Hello <span style="color:blue">{}</span>!</h1>'.format(user)


if __name__ == '__main__':
    app.run(debug=True)
