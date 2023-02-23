from flask import Flask, views

app = Flask(__name__)


def auth(func):
    def inner(*args, **kwargs):
        print('before')
        result = func(*args, **kwargs)
        print('after')
        return result

    return inner


class IndexView(views.MethodView):
    methods = ['GET', 'POST']  # 指定允许的请求方法
    decorators = [auth, ]  # 认证函数，加多个就是从上往下的效果

    def get(self):
        return "我是get请求"

    def post(self):
        return '我是post请求'


app.add_url_rule('/', view_func=IndexView.as_view('index'))  # 路由注册
