from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    # 应用场景
    # 1.Flask源码就使用了偏函数
    # 2.int函数的进制转换
    import functools
    # 八进制 到 十进制
    int8 = functools.partial(int, base=8)
    print(int8('12'))
    return 'index'


if __name__ == '__main__':
    app.run()
