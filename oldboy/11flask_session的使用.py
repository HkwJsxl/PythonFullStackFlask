import os

from flask import Flask, session
from flask_session import RedisSessionInterface
import redis

app = Flask(__name__)
conn = redis.Redis(password=os.getenv('REDIS_PASSWORD'))
# RedisSessionInterface-->redis缓存session
# use_signer-->是否对key签名
# key_prefix-->缓存key值前缀
app.session_interface = RedisSessionInterface(conn, key_prefix='hkw')


@app.route('/')
def index():
    session['key'] = 'Python666'
    return 'index'


if __name__ == '__main__':
    app.run()
