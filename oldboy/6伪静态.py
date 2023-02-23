from flask import Flask

app = Flask(__name__)


@app.route('/index.html')
def index():
    """
    伪静态就是在页面路径后面加上静态的 .html让url看着像一个静态页面
    """
    return 'index.html'


if __name__ == '__main__':
    app.run()
