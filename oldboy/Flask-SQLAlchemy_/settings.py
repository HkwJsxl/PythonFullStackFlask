import os


class BaseConfig(object):
    SESSION_TYPE = 'redis'  # session类型为redis
    SESSION_KEY_PREFIX = 'session:'  # 保存到session中的值的前缀
    SESSION_PERMANENT = True  # 如果设置为False，则关闭浏览器session就失效。
    SESSION_USE_SIGNER = True  # 是否对发送到浏览器上 session:cookie值进行加密

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://%s:%s@127.0.0.1:3306/%s?charset=utf8" % (
        'root', os.getenv('MYSQL_PASSWORD'), 'flasktest'  # 用户名，mysql密码和数据库名
    )
    SQLALCHEMY_POOL_SIZE = 15  # 数据库池的大小，默认值为5
    SQLALCHEMY_POOL_TIMEOUT = 30  # 连接超时时间
    SQLALCHEMY_POOL_RECYCLE = -1  # 回收
    SQLALCHEMY_MAX_OVERFLOW = 0  # 控制在连接池达到最大值后可以创建的连接数。当这些额外的连接回收到连接池后将会被断开和抛弃。

    # 追踪对象的修改并且发送信号
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(BaseConfig):
    pass


class DevelopmentConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass
