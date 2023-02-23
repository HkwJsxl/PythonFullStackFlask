import os

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

from models import UserInfo, Person, Hobby, Boy, Girl, Boy2Girl

engine = create_engine(
    "mysql+pymysql://%s:%s@127.0.0.1:3306/%s?charset=utf8" % (
        'root', os.getenv('MYSQL_PASSWORD'), 'flasktest'  # 用户名，mysql密码和数据库名
    ),
    max_overflow=0, pool_size=5, pool_timeout=30,
)
Session = sessionmaker(bind=engine)
session = scoped_session(Session)
# session = Session()

# 1 一对多插入数据
# obj = Hobby(name='钢琴')
# session.add(obj)
# session.commit()
# p = Person(name='张三', hobby=1)
# session.add(p)
# session.commit()
# 2 方式二(默认情况不能传对象)
# 传对象Person表中要加 hobbys = relationship('Hobby', backref='hobbys')
# p = Person(name='小李', hobbys=Hobby(name='美女'))
# session.add(p)
# 等同于
# p=Person(name='hzh')
# p.hobbys=Hobby(name='泡椒')
# session.add(p)
# 3 方式三，通过反向操作
# hb = Hobby(name='旅游')
# hb.hobbys = [Person(name='lll'), Person(name='hhh')]
# session.add(hb)

# 4 查询（查询：基于连表的查询，基于对象的跨表查询）
# 4.1 基于对象的跨表查询(子查询，两次查询)
# 正查
# p = session.query(Person).filter_by(name='hkw').first()
# print(p)
# print(p.hobbys.name)
# 反查
# h = session.query(Hobby).filter_by(name='旅游').first()
# print(h.hobbys)

# 4.2 基于连表的跨表查（查一次）
"""
# 默认根据外键连表
# isouter=True 左外连，表示Person left join Hobby，没有右连接，反过来即可
# 不写是inner join
"""
# select * from person left join hobby on person.hobby=hobby.id
# person_list = session.query(Person, Hobby).join(Hobby, isouter=True)
# print(person_list)
# for row in person_list:
#     print(row[0].name, row[1].name)
# 等同于
# select * from person, hobby where person.hobby=hobby.id
# ret = session.query(Person, Hobby).filter(Person.hobby == Hobby.id)
# print(ret)

# join表，默认是inner join
# ret = session.query(Person).join(Hobby)
# print(ret)
# ret = session.query(Hobby).join(Person, isouter=True)
# print(ret)

# 指定连表字段（了解，用不到）
# ret = session.query(Person).join(Hobby, Person.id == Hobby.id, isouter=True)
# print(ret)

# 组合（了解）UNION 操作符用于合并两个或多个 SELECT 语句的结果集
# union和union all的区别(union去重，union all只管拼接到一起)
# res = session.query(UserInfo.name).filter(UserInfo.id > 2).all()
# print(res)
# res = session.query(UserInfo.name).filter(UserInfo.id < 8).all()
# print(res)
"""
[('小刘777',), ('王五777',), ('hkw',), ('jon',), ('6ge',), ('hkw',)]
[('老王777',), ('小刘777',), ('王五777',)]
"""
# q1 = session.query(UserInfo.id, UserInfo.name).filter(UserInfo.id > 2)
# q2 = session.query(UserInfo.id, UserInfo.name).filter(UserInfo.id < 8)
# ret = q1.union_all(q2).all()
# ret1 = q1.union(q2).all()
# print(ret)
# print(ret1)
"""
[(6, '小刘777'), (7, '王五777'), (8, 'hkw'), (9, 'jon'), (10, '6ge'), (11, 'hkw'), (2, '老王777'), (6, '小刘777'), (7, '王五777')]
[(6, '小刘777'), (7, '王五777'), (8, 'hkw'), (9, 'jon'), (10, '6ge'), (11, 'hkw'), (2, '老王777')]
"""

# 多对多
# session.add_all([
#     Boy(name='霍建华'),
#     Boy(name='胡歌'),
#     Girl(name='刘亦菲'),
#     Girl(name='林心如'),
# ])
# session.commit()
# session.add_all([
#     Boy2Girl(girl_id=1, boy_id=1),
#     Boy2Girl(girl_id=2, boy_id=1)
# ])
# session.commit()

# 要有字段girls = relationship('Girl', secondary='boy2girl', backref='boys')
# girl = Girl(name='章若楠')
# girl.boys = [Boy(name='周杰伦'), Boy(name='张杰')]
# session.add(girl)
# session.commit()
# boy = Boy(name='ai坤')
# boy.girls = [Girl(name='谢娜'), Girl(name='王欣雨')]
# session.add(boy)
# session.commit()

# 基于对象的跨表查
# girl = session.query(Girl).filter_by(id=3).first()
# print(girl.boys)

# 基于连表的跨表查询
# 查询胡歌约过的所有妹子
# select girl.name from girl,boy,boy2girl where girl.id=boy2girl.boy_id,boy.id=boy2girl.girl_id and boy.name='胡歌'
# ret = session.query(Girl.name).filter(
#     Boy.id == Boy2Girl.boy_id, Girl.id == Boy2Girl.girl_id, Boy.name == '胡歌'
# ).all()
# print(ret)
"""
# select girl.name from girl 
    # inner join boy2girl on girl.id=boy2girl.girl_id 
    # inner join boy on boy.id=boy2girl.boy_id
    # where boy.name='胡歌'
"""
# ret=session.query(Girl.name).join(Boy2Girl).join(Boy).filter(Boy.name=='胡歌')
# print(ret)
# ret = session.query(Girl.name).join(Boy2Girl).join(Boy).filter_by(name='胡歌')
# print(ret)

# 执行原生sql
# django中orm如何执行原生sql(models.UserInfo.objects.row)
# from sqlalchemy.sql import text
# with engine.connect() as conn:
#     cursor = session.execute(text('select name from userinfo where name=:name'), params={'name': 'hkw'})
#     print(cursor)
#     print(cursor.first())

session.commit()
session.close()
