import os
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship
# 字段和字段属性
from sqlalchemy import (
    ForeignKey, Column, Integer, String, Text, DateTime, UniqueConstraint, Index
)

# 制造了一个类，作为所有模型类的基类(操作只管理继承Base模型类的表)
Base = declarative_base()


class UserInfo(Base):
    # mysql中主键自动建索引：聚簇索引
    # 其他键建的索引叫：辅助索引
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)  # id 主键
    name = Column(String(32), index=True, nullable=False)  # name列，索引，不可为空
    email = Column(String(32), unique=True, nullable=True)  # 唯一
    # datetime.datetime.now不能加括号，加了括号，以后永远是当前时间
    create_time = Column(DateTime, default=datetime.datetime.now)
    introduction = Column(Text, nullable=True)

    __tablename__ = 'userinfo'  # 数据库表名称，如果不写，默认以类名小写作为表的名字
    # 类似于django的 class Meta
    __table_args__ = (
        UniqueConstraint('id', 'name', name='uix_id_name'),  # 联合唯一
        Index('ix_id_name', 'name', 'email'),  # 索引
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Person(Base):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(32), index=True, nullable=False)
    # 强制写好一对多
    # 一个Hobby可以有很多人喜欢，一个人只能由一个Hobby
    hobby = Column(Integer, ForeignKey("hobby.id"))  # 默认可以为空
    # 跟数据库无关，不会新增字段，只用于快速链表操作
    # 类名，backref用于反向查询
    hobbys = relationship('Hobby', backref='hobbys')
    """hobby是整数(连接hobby的id)，hobbys是对象(跨表)"""
    __tablename__ = 'person'

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Hobby(Base):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(64), index=True, nullable=False, default='编程')

    __tablename__ = 'hobby'

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


# 多对多关系(实实在在存在的表)
class Boy2Girl(Base):
    __tablename__ = 'boy2girl'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    girl_id = Column(Integer, ForeignKey('girl.id'))
    boy_id = Column(Integer, ForeignKey('boy.id'))


class Girl(Base):
    __tablename__ = 'girl'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(64), unique=True, nullable=False)


class Boy(Base):
    __tablename__ = 'boy'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(64), unique=True, nullable=False)

    # 与生成表结构无关，仅用于查询方便,放在哪个单表中都可以
    # secondary 通过哪个表建关联，跟django中的through一模一样
    girls = relationship('Girl', secondary='boy2girl', backref='boys')


def create_table():
    # 创建engine对象
    engine = create_engine(
        "mysql+pymysql://%s:%s@127.0.0.1:3306/%s?charset=utf8" % (
            'root', os.getenv('MYSQL_PASSWORD'), 'flasktest'  # 用户名，mysql密码和数据库名
        ),
        max_overflow=0,  # 超过连接池大小外最多创建的连接
        pool_size=5,  # 连接池大小
        pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
        pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
    )
    # 通过engine对象创建表
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_table()
