from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .views import account

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('settings.DevelopmentConfig')

    # 将db注册到app中
    db.init_app(app)

    # 注册蓝图
    app.register_blueprint(account.account)

    return app
