import os

from flask import Flask
from flask_admin import Admin

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine(
    "mysql+pymysql://%s:%s@127.0.0.1:3306/%s?charset=utf8" % (
        'root', os.getenv('MYSQL_PASSWORD'), 'flasktest'  # 用户名，mysql密码和数据库名
    ),
    max_overflow=0, pool_size=5, pool_timeout=30,
)
Session = sessionmaker(bind=engine)
session = scoped_session(Session)

app = Flask(__name__)
# 将app注册到admin中
admin = Admin(app)

if __name__ == "mian":
    app.run()
    # 访问127.0.0.1:5000/admin端口，会得到一个空白的页面
