from flask import Flask, signals

app = Flask(__name__)


def func(*args, **kwargs):
    print(args[0])  # 当前app对象
    print('触发信号', args, kwargs)


# 往信号中注册函数
signals.request_started.connect(func)


@app.route('/', methods=['GET', "POST"])
def index():
    return 'index'


if __name__ == '__main__':
    app.wsgi_app
    app.run()
