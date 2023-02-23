from flask import Flask, g

app = Flask(__name__)


@app.before_request
def bfr():
    """
    g对象只存在于当前的请求中，请求结束，对象销毁
    """
    g.name = 'hkw'


@app.route('/index1')
def index1():
    print(g.name)
    return 'index1页面'


@app.route('/index2')
def index2():
    """
    两次请求中的值不是一个
    """
    print(g.name)
    return 'index2页面'


if __name__ == '__main__':
    app.run()
