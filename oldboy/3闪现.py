from flask import Flask, flash, get_flashed_messages

app = Flask(__name__)
app.secret_key = '及时行乐'


@app.route('/')
def push():
    # 原理
    # 把值放到了session中，所以必须要设置app.secret_key

    # 可以加category参数,取值时只能取指定分类中的值
    flash({'name': 'hkw'})
    return '放置成功'


@app.route('/pull')
def pull():
    res = get_flashed_messages('name')
    print(res)  # [('message', {'name': 'hkw'})]
    return res or '没有值了'


if __name__ == '__main__':
    app.run()
