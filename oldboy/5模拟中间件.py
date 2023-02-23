from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World!'


# 模拟中间件
class Md(object):
    def __init__(self, old_wsgi_app):
        self.old_wsgi_app = old_wsgi_app

    def __call__(self, environ, start_response):
        print('开始之前')
        ret = self.old_wsgi_app(environ, start_response)
        print('结束之后')
        return ret


if __name__ == '__main__':
    # 1 我们发现当执行app.run方法的时候，最终执行run_simple，最后执行app(),也就是在执行app.__call__方法
    # 2 在__call__里面，执行的是self.wsgi_app().那我们希望在执行他本身的wsgi之前做点事情。
    # 3 所以我们先用Md类中__init__，保存之前的wsgi,然后我们用将app.wsgi转化成Md的对象。
    # 4 那执行新的的app.wsgi_app，就是执行Md的__call__方法。
    # 把原来的wsgi_app替换为自定义的，
    app.wsgi_app = Md(app.wsgi_app)
    app.run()
