from flask import Flask
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/test')
def test():
    return 'Just testing...'

@app.route('/date/ts')
def date_ts():
    d = datetime.now()
    return str(d.timestamp())

@app.route('/date/iso')
def date_iso():
    d = datetime.now()
    return d.isoformat()

@app.route('/say_hello/<name>')
def say_hello(name):
    return 'Hello ' + name + '!'

if __name__ == '__main__':
    app.run()
