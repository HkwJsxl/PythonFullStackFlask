from flask import Blueprint

from .. import models
from .. import db

account = Blueprint('account', __name__)


@account.route('/')
def login():
    # 添加数据
    db.session.add(models.UserInfo(username='hkw', email='hkw@hkw.com'))
    db.session.add(models.UserInfo(username='root', email='root@root.com'))
    db.session.commit()
    db.session.close()
    # 查询数据
    user_list = db.session.query(models.UserInfo).all()
    print(user_list)
    for item in user_list:
        print(item.username)

    return 'login'
