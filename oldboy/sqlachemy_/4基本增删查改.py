import os

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

from models import UserInfo, Person, Hobby

engine = create_engine(
    "mysql+pymysql://%s:%s@127.0.0.1:3306/%s?charset=utf8" % (
        'root', os.getenv('MYSQL_PASSWORD'), 'flasktest'  # 用户名，mysql密码和数据库名
    ),
    max_overflow=0, pool_size=5, pool_timeout=30,
)
Session = sessionmaker(engine)
session = scoped_session(Session)
# session = Session()

# 1.新增多个对象
# obj = UserInfo(name='张三')
# obj2 = UserInfo(name='里斯')
# obj3 = UserInfo(name='王五')
# 新增同样对象
# session.add_all([
#   obj, obj2, obj3
# ])
# 新增不同对象
# session.add_all([
#     Person(name='lin', hobby=3), Hobby(name='篮球')
# ])
# 2.简单删除（查到删除）
# session.query(UserInfo).filter_by(name='hkw').delete()
# session.query(UserInfo).filter(UserInfo.id>=3).delete()
# 3.修改
# session.query(UserInfo).filter_by(id=2).update({UserInfo.name:'老王'})
# session.query(UserInfo).filter_by(id=6).update({'name':'小刘'})
# 高级修改
# session.query(UserInfo).filter(UserInfo.id > 0).update(
#     {UserInfo.name: UserInfo.name + "777"}, synchronize_session=False
# )  # 如果要把它转成字符串相加
# session.query(UserInfo).filter(UserInfo.id > 0).update(
#     {"age": UserInfo.age + 1}, synchronize_session="evaluate"
# )  # 如果要把它转成数字相加

# 4.基本查询操作
# res=session.query(UserInfo).all()
# print(res)
# res=session.query(UserInfo).first()
# print(res)

# filter传的是表达式，filter_by传的是参数
# res=session.query(UserInfo).filter(UserInfo.id>=2).all()
# print(res)
# res=session.query(UserInfo).filter_by(name='hkw').all()
# print(res)

# 了解(自定义SQL语句)
# res = session.query(UserInfo).from_statement(
#     text("SELECT * FROM UserInfo where name=:name")
# ).params(name='hkw').all()
# print(res)

session.commit()
# 并没有真正关闭连接，而是放回池中
session.close()
