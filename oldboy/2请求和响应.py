from flask import Flask, request, make_response, jsonify, render_template, redirect

app = Flask(__name__)


@app.route('/')
def index():
    """请求"""
    print(request.method)  # 提交的方法
    print(request.args)  # get请求提及的数据
    print(request.form)  # post请求提交的数据
    print(request.values)  # post和get提交的数据总和
    print(request.values.getlist('name'))  # get和list的key一样是要用getlist
    print(request.cookies)  # 客户端所带的cookie
    print(request.headers)  # 请求头
    print(request.path)  # 不带域名，不带参数请求路径
    print(request.full_path)  # 不带域名，带参数的请求路径
    print(request.url)  # 带域名带参数的请求路径
    print(request.base_url)  # 带域名请求路径
    print(request.url_root)  # 带域名请求路径
    print(request.host_url)  # 带域名请求路径
    print(request.host)  # 127.0.0.1:5000
    print(request.files)  # 上传的文件
    # return 'Index'
    """响应"""
    # return "字符串"
    # return render_template('html模板路径',**{})
    # return redirect('/index/')
    return jsonify({'name': 'hkw'})
    # res = make_response()  # 制作响应对象
    # res.set_cookie('key', 'value')
    # res.headers['X-Token'] = 'respon2请求和响应.pyseXXX'
    # res.delete_cookie('key')


if __name__ == '__main__':
    app.run()
