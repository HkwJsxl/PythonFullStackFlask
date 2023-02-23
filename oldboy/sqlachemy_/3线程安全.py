# 基于scoped_session实现线程安全

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from models import UserInfo

# 1 制作engine
engine = create_engine(
    "mysql+pymysql://%s:%s@127.0.0.1:3306/%s?charset=utf8" % (
        'root', os.getenv('MYSQL_PASSWORD'), 'flasktest'  # 用户名，mysql密码和数据库名
    ),
    max_overflow=0, pool_size=5, pool_timeout=30,
)
# 2 制造一个 session 类（会话）
Session = sessionmaker(bind=engine)  # 得到一个类
# 3 得到一个session对象（线程安全的session）
# 现在的session已经不是session对象了
# 为什么线程安全，还是用的local
session = scoped_session(Session)
# 4 创建一个对象
obj1 = UserInfo(name="hkw")
# 5 把对象通过add放入
session.add(obj1)
# 6 提交
session.commit()
session.close()
