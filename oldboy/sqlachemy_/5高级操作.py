import os

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy import and_, or_
from sqlalchemy.sql import func  # 分组
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

# 1 查询名字为hkw的所有UserInfo对象
# res = session.query(UserInfo).filter_by(name='hkw').all()
# print(res)
# 2 表达式，and条件连接
# res = session.query(UserInfo).filter(UserInfo.id > 1, UserInfo.name == 'hkw').all()
# print(res)
# 查找id在1和10之间，并且name=hkw的对象
# res = session.query(UserInfo).filter(UserInfo.id.between(1, 10), UserInfo.name == 'hkw').all()
# print(res)
# in条件(class_,因为这是关键字，不能直接用)
# res = session.query(UserInfo).filter(UserInfo.id.in_([2, 3, 9])).all()
# print(res)
# 取反 ~
# res = session.query(UserInfo).filter(~UserInfo.id.in_([2, 3, 9])).all()
# print(res)
# 二次筛选
# select * ...
# res = session.query(Person).filter(Person.hobby.in_(session.query(Hobby.id).filter(Hobby.name=='编程'))).all()
# print(res)
# select id,name ...
# res = session.query(Person.id, Person.name).filter(
#     Person.hobby.in_(session.query(Hobby.id).filter(Hobby.name == '编程'))
# ).all()
# print(res)

# or_包裹的都是or条件，and_包裹的都是and条件
# 查询id>3并且name=hkw的人
# res = session.query(UserInfo).filter(and_(UserInfo.id > 3, UserInfo.name == 'hkw')).all()
# print(res)
# 查询id小于等于3或者name=hkw的数据
# res = session.query(UserInfo).filter(or_(UserInfo.id <= 3, UserInfo.name == 'hkw')).all()
# print(res)
# 查询 name=hkw并且id大于3 或者 id小于等于3的数据
# res = session.query(UserInfo).filter(
#     or_(
#         UserInfo.id <= 3,
#         and_(UserInfo.name == 'hkw', UserInfo.id > 3)
#     )).all()
# print(res)

# 通配符，以h开头，不以h开头
# res = session.query(UserInfo).filter(UserInfo.name.like('h%')).all()
# print(res)
# res = session.query(UserInfo).filter(~UserInfo.name.like('h%')).all()
# print(res)

# 排序，根据name降序排列（从大到小）
# res = session.query(UserInfo).order_by(UserInfo.name.desc()).all()
# print(res)
# res = session.query(UserInfo).order_by(UserInfo.name.asc()).all()
# print(res)
# 第一个条件降序排序后，再按第二个条件升序排
# res = session.query(UserInfo.id, UserInfo.name).order_by(UserInfo.name.desc(), UserInfo.id.asc()).all()
# print(res)

# 分组
# from sqlalchemy.sql import func
# sql分组之后，要查询的字段中只能有分组字段和聚合函数
# res = session.query(UserInfo.introduction, func.count(UserInfo.name)).group_by(UserInfo.introduction).all()
# print(res)
"""
from userinfo.introduction, count(userinfo.name) from userinfo group by userinfo.introduction
"""

# haviing筛选
# res = session.query(
#     UserInfo.introduction, func.count(UserInfo.id)
# ).group_by(
#     UserInfo.introduction
# ).having(
#     func.count(UserInfo.id) > 2
# ).all()
# print(res)
"""
from userinfo.introduction, count(userinfo.id) from userinfo group by userinfo.introduction having count(userinfo.id)>2
"""

session.commit()
session.close()
