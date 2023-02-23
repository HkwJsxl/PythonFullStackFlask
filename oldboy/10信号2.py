from flask import Flask
from flask.signals import _signals

app = Flask(__name__)

xxx = _signals.signal('xxx')


def func(sender, *args, **kwargs):
    # 发送过来的消息
    print('sender', sender)
    print(args, kwargs)
    """
    sender 666
    () {'name': 'hkw', 'age': '20'}
    """


# 自定义信号中注册函数
xxx.connect(func)


@app.route("/")
def index():
    # 触发信号(只能有一个位置参数，可以有多个关键字参数)
    xxx.send('666', name='hkw', age='20')
    return 'index'


if __name__ == '__main__':
    app.run()
