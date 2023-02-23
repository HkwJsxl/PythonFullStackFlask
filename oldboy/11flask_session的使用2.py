"""
运行：python .\12flask-script的使用.py runserver
"""
import os

from flask import Flask, session
from redis import Redis
from flask_session import Session

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = Redis(password=os.getenv('REDIS_PASSWORD'))
Session(app)


@app.route('/')
def index():
    session['key'] = 'Python666'
    return 'index'


if __name__ == '__main__':
    app.run()
