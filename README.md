
# Flask知识

Github地址：`https://github.com/HkwJsxl`
博客园地址：`https://www.cnblogs.com/hkwJsxl/`

## 导入

~~~python
from flask import (
    Flask,request,render_template,redirect,session,url_for,Markup,make_response,views,jsonify,
    flash,get_flashed_messages,g
)
request  # 传过来的请求
render_template  # 模板
redirect  # 重定向，可配合url_for
url_for  # 反向解析
session  # 使用前要先设置密钥：app.secret_key=''
Markup  # 处理XSS攻击
make_response  # 制作响应对象
views  # CBV继承views.MethodView
flash  # 闪现设值
get_flashed_messages  # 闪现取值
g  # 全局变量，当前请求中放值，取值
~~~

## route和dtl

~~~python
# 路由
# @app.route和app.add_url_rule参数
strict_slashes=False  # 对url最后的 / 是否做严格要求，默认严格
redirect_to='login/'  # 重定向到指定地址
methods=['GET', 'POST', ]  # 支持的请求方式
endpoint='login'  # 别名，如果不写默认是函数名，并且不能重名
subdomain = None  # 子域名访问
# 路由的本质就是：app.add_url_rule()

# 模板语言渲染同dtl，但比dtl更加强大，支持函数加括号执行，字典支持点取值、括号取值和get取值
~~~

## 配置文件

~~~python
# 配置方式
1.app.config['DEBUG'] = True  # debug为True可能会无效，edit configurations-->勾选FLASK_DEBUG
2.通过文件配置
app.config.from_pyfile("settings.py")
app.config.from_json("settings.json")
3.类（常用）
app.config.from_object('settings.DevelopmentConfig')
settings.py
class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'
class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'
class DevelopmentConfig(Config):
    DEBUG = True
PS: 从sys.path中已经存在路径开始写
PS: settings.py文件默认路径要放在程序root_path目录，如果instance_relative_config为True，则就是instance_path目录（Flask对象init方法的参数）

# 配置
flask中的配置文件是一个flask.config.Config对象（继承字典）,默认配置为：
{
    'DEBUG':                                get_debug_flag(default=False),  是否开启Debug模式
    'TESTING':                              False,                          是否开启测试模式
    'PROPAGATE_EXCEPTIONS':                 None,                          
    'PRESERVE_CONTEXT_ON_EXCEPTION':        None,
    'SECRET_KEY':                           None,
    'PERMANENT_SESSION_LIFETIME':           timedelta(days=31),
    'USE_X_SENDFILE':                       False,
    'LOGGER_NAME':                          None,
    'LOGGER_HANDLER_POLICY':               'always',
    'SERVER_NAME':                          None,
    'APPLICATION_ROOT':                     None,
    'SESSION_COOKIE_NAME':                  'session',
    'SESSION_COOKIE_DOMAIN':                None,
    'SESSION_COOKIE_PATH':                  None,
    'SESSION_COOKIE_HTTPONLY':              True,
    'SESSION_COOKIE_SECURE':                False,
    'SESSION_REFRESH_EACH_REQUEST':         True,
    'MAX_CONTENT_LENGTH':                   None,
    'SEND_FILE_MAX_AGE_DEFAULT':            timedelta(hours=12),
    'TRAP_BAD_REQUEST_ERRORS':              False,
    'TRAP_HTTP_EXCEPTIONS':                 False,
    'EXPLAIN_TEMPLATE_LOADING':             False,
    'PREFERRED_URL_SCHEME':                 'http',
    'JSON_AS_ASCII':                        True,
    'JSON_SORT_KEYS':                       True,
    'JSONIFY_PRETTYPRINT_REGULAR':          True,
    'JSONIFY_MIMETYPE':                     'application/json',
    'TEMPLATES_AUTO_RELOAD':                None,
}
~~~

## 转换器

~~~python
DEFAULT_CONVERTERS = {
    'default':          UnicodeConverter,
    'string':           UnicodeConverter,
    'any':              AnyConverter,
    'path':             PathConverter,
    'int':              IntegerConverter,
    'float':            FloatConverter,
    'uuid':             UUIDConverter,
}
@app.route('/detail/<int:pk>', methods=['GET'])
~~~

## CBV

~~~python
"""示例"""
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
~~~

## 请求和响应

~~~python
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
    # res.headers['X-Token'] = 'responseXXX'
    # res.delete_cookie('key')
if __name__ == '__main__':
    app.run()
~~~

## 闪现

~~~python
flash('')  # 设置值，可以加category参数
get_flashed_message()  # 取值，取出分类category_filter=['', '']
# 原理
把值放到了session中，所以必须要设置app.secret_key
# 应用场景
假设在a页面操作出错，跳转到b页面，在b页面显示a页面的错误信息

"""示例"""
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
~~~

## 请求扩展

~~~python
# 类似于django的中间件
@app.before_request：请求来的时候执行，类似于Django的process_request，多个是从上往下执行
@app.after_request：请求走的时候执行，类似于Django的process_response，多个是从下往上执行
@app.before_first_request(即将过时)：项目第一次启动来请求时执行，只执行一次，也可以配多个
@app.teardown_request：每次视图函数执行完都会执行，即使报错也会执行，可用来记录日志
@app.errorhandler(404)：绑定错误的状态码，只要码匹配，就执行
@app.template_global：全局标签
@app.template_filter：全局过滤器
# before_request请求拦截后（也就是有return值），所有的after_request（response）都会执行，Django中请求拦截后，从当前位置拦截响应回去
# 示例
@app.before_request
def before():
    print('before')
@app.after_request
def after(response):
    print('after')
    return response
@app.before_first_request
def first():
    print('first')
@app.teardown_request
def teardown(*args, **kwargs):
    # print('teardown', args)
    # print('teardown', kwargs)
    print('teardown')
@app.errorhandler(404)
def error_404(*args, **kwargs):
    print('errorhandler404', args)
    # print('errorhandler404', kwargs)
    return render_template('errors.html', message=args[0])
@app.template_global()
def a(a1, a2):
    return a1 + a2
@app.template_filter()
def b(a1, a2, a3):
    return a1 + a2 + a3
# errors.html
<h3>{{ message }}</h3>
{{ a(1,2) }}
{{ 1|b(2,3) }}
~~~

## 中间件

~~~python
from flask import Flask
app = Flask(__name__)
@app.route('/')
def index():
    return 'Hello World!'
# 模拟中间件
class Md(object):
    def __init__(self,old_wsgi_app):
        self.old_wsgi_app = old_wsgi_app
    def __call__(self,  environ, start_response):
        print('开始之前')
        ret = self.old_wsgi_app(environ, start_response)
        print('结束之后')
        return ret
if __name__ == '__main__':
    #1 我们发现当执行app.run方法的时候，最终执行run_simple，最后执行app(),也就是在执行app.__call__方法	
    #2 在__call__里面，执行的是self.wsgi_app().那我们希望在执行他本身的wsgi之前做点事情。
    #3 所以我们先用Md类中__init__，保存之前的wsgi,然后我们用将app.wsgi转化成Md的对象。
    #4 那执行新的的app.wsgi_app，就是执行Md的__call__方法。
    #把原来的wsgi_app替换为自定义的，
    app.wsgi_app = Md(app.wsgi_app)
    app.run()
~~~

## 补充

### 猴子补丁

~~~python
# 什么是猴子补丁？
# 只是一个概念，不属于任何包和模块
# 利用了python一切皆对象的理念，在程序运行过程中，动态修改方法
# 有什么用？
# 这里有一个比较实用的例子,
# 很多用到import json,
# 后来发现ujson性能更高,
# 如果觉得把每个文件的import json改成import ujson as json成本较高,
# 或者说想测试一下ujson替换是否符合预期, 只需要在入口加上:

# 只需要在程序入口
# import json
# import ujson
# def monkey_patch_json():
#     json.__name__ = 'ujson'
#     json.dumps = ujson.dumps
#     json.loads = ujson.loads
# monkey_patch_json()
# 以后用的json操作就是ujson
~~~

### 伪静态

~~~python
伪静态就是在页面路径后面加上静态的 .html
让url看着像一个静态页面
~~~

## 蓝图

~~~python
# 目录结构
-blueprint
    -templates文件夹
    -views包
    	-__init__.py
    	-user.py
    manage.py

# 使用
1.在app中注册蓝图，括号里是一个蓝图对象
app.register_blueprint(user.account)
2.第二步，在不同文件中注册路由时，直接使用蓝图对象注册，不用使用app了，避免了循环导入的问题
from flask import Blueprint
account = Blueprint('user', __name__, url_prefix='/xxx', template_folder='xxx')
# url_prefix：给当前蓝图下的url都加上统一的前缀
# template_folder：每个蓝图可以设置自己的templates
3.写视图
@account.route('/login.html', methods=['GET', "POST"])
# 蓝图的befort_request，只对当前蓝图有效

"""示例"""
# manage.py
from flask import Flask
from oldboy.blueprint.views import user
app = Flask(__name__)
app.register_blueprint(user.account)
if __name__ == '__main__':
    app.run()
# user.py
from flask import Blueprint
account = Blueprint('user', __name__, url_prefix='/user', template_folder='templates')
# http://127.0.0.1:5000/user/
@account.route('/', methods=['GET'])
def index():
    return 'index'
~~~

## 分析

### session源码的执行流程

~~~python
# save_seesion
-响应的时候，把session中的值加密序列化放到了cookie中，返回到浏览器中
# open_session
-请求来了，从cookie中取出值，反解，生成session对象，以后再视图函数中直接用sessoin就可以了。
~~~

### 请求上下文源码分析

~~~python
第一阶段：将ctx(request,session)放到Local对象上
第二阶段：视图函数导入：request/session
request.method
	-LocalProxy对象.method,执行getattr方法，getattr(self._get_current_object(), name)
		-self._get_current_object()返回return self.__local()，self.__local()，在LocakProxy实例化的时候,object.__setattr__(self, '_LocalProxy__local', local),此处local就是：partial(_lookup_req_object, 'request')

	-def _lookup_req_object(name):
			top = _request_ctx_stack.top  # _request_ctx_stack 就是LocalStack()对象，top方法把ctx取出来
			if top is None:
				raise RuntimeError(_request_ctx_err_msg)
			return getattr(top, name)  # 获取ctx中的request或session对象

第三阶段：请求处理完毕
		- 获取session并保存到cookie
		- 将ctx删除

程序运行，两个LocalStack()对象，一个里面放request和session，另一个放g和current_app
~~~

## g对象

~~~python
# g对象是全局对象，只用于当前请求存放值，请求结束时g对象也同时销毁

# g对象和session的区别
session对象是可以跨request的，只要session还未失效，不同的request的请求会获取到同一个session，
但是g对象不是，g对象不需要管过期时间，请求一次就g对象就改变了一次，或者重新赋值了一次（g对象是针对于当前请求的）

"""示例"""
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
~~~

## 偏函数

~~~python
partial，作用是给函数一个默认的参数，把该参数给固定住
# 应用场景
1.Flask源码就使用了偏函数
2.int函数的进制转换
# 八进制到十进制
import functools
int8 = functools.partial(int,base=8)
print(int8('12'))
~~~

## 数据库连接池

~~~python
-settings
	-mysql_config.py
-start.py

"""mysql_config.py"""
import os
from datetime import timedelta
import pymysql
# Python3不能适配DBUtils 2.0及以上版本，需要安装1.X版本
# pip install DBUtils==1.4
from DBUtils.PooledDB import PooledDB
class Config(object):
    DEBUG = True
    SECRET_KEY = "SECRET_KEY-SECRET_KEY-SECRET_KEY"
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=15)
    SESSION_REFRESH_EACH_REQUEST = True
    SESSION_TYPE = "mysql"
    PYMYSQL_POOL = PooledDB(
        creator=pymysql,  # 使用链接数据库的模块
        maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
        mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
        maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
        maxshared=3,
        # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
        blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
        maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
        setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
        ping=0,
        # ping MySQL服务端，检查是否服务可用。
        # 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
        host='127.0.0.1',
        port=3306,
        user='root',
        password=os.getenv('MYSQL_PASSWORD'),
        database='flasktest',
        charset='utf8'
    )
"""start.py"""
import pymysql
from settings.mysql_config import Config
class SQLHelper(object):
    @staticmethod
    def open(cursor):
        POOL = Config.PYMYSQL_POOL
        conn = POOL.connection()
        cursor = conn.cursor(cursor=cursor)
        return conn, cursor
    @staticmethod
    def close(conn, cursor):
        conn.commit()
        cursor.close()
        conn.close()
    @classmethod
    def fetch_one(cls, sql, args=None, cursor=pymysql.cursors.DictCursor):
        conn, cursor = cls.open(cursor)
        cursor.execute(sql, args)
        obj = cursor.fetchone()
        cls.close(conn, cursor)
        return obj
    @classmethod
    def fetch_all(cls, sql, args=None, cursor=pymysql.cursors.DictCursor):
        conn, cursor = cls.open(cursor)
        cursor.execute(sql, args)
        obj = cursor.fetchall()
        cls.close(conn, cursor)
        return obj
    @classmethod
    def execute(cls, sql, args=None, cursor=pymysql.cursors.DictCursor):
        conn, cursor = cls.open(cursor)
        cursor.execute(sql, args)
        cls.close(conn, cursor)
if __name__ == '__main__':
    obj = SQLHelper.fetch_all("select id, name from t1;")
    print(obj)
~~~

## wtforms（forms组件）

~~~python
# 安装：pip3 install wtforms
# 作用
1.校验数据
2.渲染标签
~~~

### 登录

login.py

~~~python
from flask import Flask, render_template, request
from wtforms import Form
from wtforms.fields import simple
from wtforms import validators
from wtforms import widgets
app = Flask(__name__, template_folder='templates')
app.debug = True
class LoginForm(Form):
    # 字段（内部包含正则表达式）
    name = simple.StringField(
        label='用户名',
        validators=[
            validators.DataRequired(message='用户名不能为空.'),
            validators.Length(min=6, max=18, message='用户名长度必须大于%(min)d且小于%(max)d')
        ],
        widget=widgets.TextInput(),  # 页面上显示的插件
        render_kw={'class': 'form-control'}

    )
    # 字段（内部包含正则表达式）
    pwd = simple.PasswordField(
        label='密码',
        validators=[
            validators.DataRequired(message='密码不能为空.'),
            validators.Length(min=8, message='用户名长度必须大于%(min)d'),
            validators.Regexp(
                regex="^([a-zA-Z]+[0-9]+[,._!@#$%^&*]+)|([a-zA-Z]+[,._!@#$%^&*]+[0-9]+)|([0-9]+[,._!@#$%^&*]+[a-zA-Z]+)|([0-9]+[a-zA-Z]+[,._!@#$%^&*]+)|([,._!@#$%^&*]+[a-zA-Z]+[0-9]+)|([,._!@#$%^&*]+[0-9]+[a-zA-Z]+)$",
                message='密码至少8个字符，至少1个字母，1个数字和1个特殊字符')
        ],
        widget=widgets.PasswordInput(),
        render_kw={'class': 'form-control'}
    )
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm()
        return render_template('login.html', form=form)
    else:
        form = LoginForm(formdata=request.form)
        print(form.data)
        if form.validate():
            print('用户提交数据通过格式验证，提交的值为：', form.data)
        else:
            print(form.errors)
        return render_template('login.html', form=form)
if __name__ == '__main__':
    app.run()
~~~

login.html

~~~html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>login</title>
</head>
<body>
<h1>登录</h1>
<form method="post" novalidate style="padding:0  50px">
    {% for field in form %}
        <p>{{ field.label }}: {{ field }} {{ field.errors[0] }}</p>
    {% endfor %}
    <input type="submit" value="提交">
</form>
</body>
</html>
~~~

### 注册

register.py

~~~python
"""
邮箱验证码需要email_validator模块支持：
pip install email_validator
"""
from flask import Flask, render_template, request
from wtforms import Form
from wtforms import fields
from wtforms import validators
from wtforms import widgets
app = Flask(__name__, template_folder='templates')
app.debug = True
class RegisterForm(Form):
    name = fields.StringField(
        label='用户名',
        validators=[
            validators.DataRequired(),
            validators.Length(min=6, max=18, message='用户名长度必须大于%(min)d且小于%(max)d')
        ],
        widget=widgets.TextInput(),
        render_kw={'class': 'form-control'},
        default='anonymous'
    )
    pwd = fields.PasswordField(
        label='密码',
        validators=[
            validators.DataRequired(message='密码不能为空.'),
            validators.Length(min=8, message='用户名长度必须大于%(min)d'),
            validators.Regexp(
                regex="^([a-zA-Z]+[0-9]+[,._!@#$%^&*]+)|([a-zA-Z]+[,._!@#$%^&*]+[0-9]+)|([0-9]+[,._!@#$%^&*]+[a-zA-Z]+)|([0-9]+[a-zA-Z]+[,._!@#$%^&*]+)|([,._!@#$%^&*]+[a-zA-Z]+[0-9]+)|([,._!@#$%^&*]+[0-9]+[a-zA-Z]+)$",
                message='密码至少8个字符，至少1个字母，1个数字和1个特殊字符')
        ],
        widget=widgets.PasswordInput(),
        render_kw={'class': 'form-control'}
    )
    pwd_confirm = fields.PasswordField(
        label='重复密码',
        validators=[
            validators.DataRequired(message='重复密码不能为空.'),
            validators.Length(min=8, message='用户名长度必须大于%(min)d'),
            validators.Regexp(
                regex="^([a-zA-Z]+[0-9]+[,._!@#$%^&*]+)|([a-zA-Z]+[,._!@#$%^&*]+[0-9]+)|([0-9]+[,._!@#$%^&*]+[a-zA-Z]+)|([0-9]+[a-zA-Z]+[,._!@#$%^&*]+)|([,._!@#$%^&*]+[a-zA-Z]+[0-9]+)|([,._!@#$%^&*]+[0-9]+[a-zA-Z]+)$",
                message='密码至少8个字符，至少1个字母，1个数字和1个特殊字符'),
            validators.EqualTo('pwd', message="两次密码输入不一致")
        ],
        widget=widgets.PasswordInput(),
        render_kw={'class': 'form-control'}
    )
    email = fields.EmailField(
        label='邮箱',
        validators=[
            validators.DataRequired(message='邮箱不能为空.'),
            validators.Email(message='邮箱格式错误')
        ],
        widget=widgets.TextInput(input_type='email'),
        render_kw={'class': 'form-control'}
    )
    gender = fields.RadioField(
        label='性别',
        choices=(
            (1, '男'),
            (2, '女'),
        ),
        coerce=int
    )
    city = fields.SelectField(
        label='城市',
        choices=(
            ('bj', '北京'),
            ('sh', '上海'),
        )
    )
    hobby = fields.SelectMultipleField(
        label='爱好',
        choices=(
            (1, '篮球'),
            (2, '足球'),
        ),
        coerce=int
    )
    favor = fields.SelectMultipleField(
        label='喜好',
        choices=(
            (1, '篮球'),
            (2, '足球'),
        ),
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput(),
        coerce=int,
        default=[1, 2]
    )
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.favor.choices = ((1, '篮球'), (2, '足球'), (3, '羽毛球'))
    def validate_pwd_confirm(self, field):
        """
        自定义pwd_confirm字段规则，例：与pwd字段是否一致
        :param field:
        :return:
        """
        # 最开始初始化时，self.data中已经有所有的值

        if field.data != self.data['pwd']:
            # raise validators.ValidationError("密码不一致") # 继续后续验证
            raise validators.StopValidation("密码不一致")  # 不再继续后续验证
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        form = RegisterForm(data={'gender': 2, 'hobby': [1, ]})  # initial
        return render_template('register.html', form=form)
    else:
        form = RegisterForm(formdata=request.form)
        if form.validate():
            print('用户提交数据通过格式验证，提交的值为：', form.data)
        else:
            print(form.errors)
        return render_template('register.html', form=form)
if __name__ == '__main__':
    app.run()
~~~

register.html

~~~html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>register</title>
</head>
<body>
<h1>register</h1>
<form method="post" novalidate style="padding:0  50px">
    {% for field in form %}
        <p>{{ field.label }}: {{ field }} {{ field.errors[0] }}</p>
    {% endfor %}
    <input type="submit" value="提交">
</form>
</body>
</html>
~~~



## 信号

Flask框架中的信号基于blinker，安装：`pip install blinker`

### 内置信号种类

~~~python
request_started = _signals.signal('request-started')                # 请求到来前执行
request_finished = _signals.signal('request-finished')              # 请求结束后执行

before_render_template = _signals.signal('before-render-template')  # 模板渲染前执行
template_rendered = _signals.signal('template-rendered')            # 模板渲染后执行

got_request_exception = _signals.signal('got-request-exception')    # 请求执行出现异常时执行

request_tearing_down = _signals.signal('request-tearing-down')      # 请求执行完毕后自动执行（无论成功与否）
appcontext_tearing_down = _signals.signal('appcontext-tearing-down')# 应用上下文执行完毕后自动执行（无论成功与否）

appcontext_pushed = _signals.signal('appcontext-pushed')            # 应用上下文push时执行
appcontext_popped = _signals.signal('appcontext-popped')            # 应用上下文pop时执行
message_flashed = _signals.signal('message-flashed')                # 调用flask在其中添加数据时，自动触发
~~~

### 用法

~~~python
# 信号是同步操作

"""内置信号"""
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
    
"""自定义信号"""
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
~~~

# 第三方

## flask-session

~~~python
# 安装
pip3 install flask-session
# 使用方式一
"""
import os
from flask import Flask, session
from flask_session import RedisSessionInterface
import redis
app = Flask(__name__)
conn = redis.Redis(password=os.getenv('REDIS_PASSWORD'))
# RedisSessionInterface-->redis缓存session
# use_signer-->是否对key签名
# key_prefix-->缓存key值前缀
app.session_interface = RedisSessionInterface(conn, key_prefix='hkw')
@app.route('/')
def index():
    session['key'] = 'Python666'
    return 'index'
if __name__ == '__main__':
    app.run()

"""
# 使用方式二
"""
import os
from flask import Flask, session
from redis import Redis
from flask_session import Session
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = Redis(password=os.getenv('REDIS_PASSWORD'))
Session(app)
"""

# 不用第三方：设置cookie时，如何设定关闭浏览器则cookie失效。
response.set_cookie('k','v',exipre=None)  # 这样设置即可
# 使用第三方---permanent=False
app.session_interface = RedisSessionInterface(conn,key_prefix='前缀',permanent=False)
# Django中也是一个参数配置
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# cookie默认超时时间是多少？如何设置超时时间
'PERMANENT_SESSION_LIFETIME':timedelta(days=31)  # 这个配置文件控制
~~~

## flask-script

~~~python
# 模拟出类似django的启动方式：python manage.py runserver
# 安装：pip install flask-script
# 把excel的数据导入数据库，定制个命令，去执行(openpyxl)
	# python manage.py insertdb -f xxx.excl -t aa
# 使用
# 方式一：python manage.py runserver
import os
from flask import Flask, session
from redis import Redis
from flask_session import Session
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = Redis(password=os.getenv('REDIS_PASSWORD'))
Session(app)
@app.route('/')
def index():
    session['key'] = 'Python666'
    return 'index'
if __name__ == '__main__':
    app.run()
# 方式二：自定制命令
@manager.command
def custom(arg):
    # 无-参数
    # python manage.py custom 123
    print(arg)
@manager.option('-n', '--name', dest='name')
@manager.option('-u', '--url', dest='url')
def cmd(name, url):
    # 执行： python manage.py  cmd -n lqz -u http://www.oldboyedu.com
    # 执行： python manage.py  cmd --name lqz --url http://www.oldboyedu.com
    print(name, url)
# 应用场景
1.创建超级用户
2.现在有一万条excel用户，批量导入到数据库中
	navicate直接支持
	脚本
	flask-script
~~~

## sqlalchemy

~~~python
# sqlachemy：第三方orm框架（对象关系映射）
# 手写orm：https://www.cnblogs.com/liuqingzheng/articles/9006025.html
# 安装：pip install sqlalchemy
# SQLAlchemy本身无法操作数据库，必须基于pymsql等第三方插件
~~~

#### 基本使用（原生sql）

~~~python
import os
from sqlalchemy import create_engine
# 第一步生成一个engine对象
engine = create_engine(
    "mysql+pymysql://root:%s@127.0.0.1:3306/%s?charset=utf8" % (
        'root', os.getenv('MYSQL_PASSWORD'), 'flasktest'  # 用户名，mysql密码和数据库名
    ),
    max_overflow=0,  # 超过连接池大小外最多创建的连接
    pool_size=5,  # 连接池大小
    pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
    pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
)
# 第二步：创建连接（执行原生sql）
conn = engine.raw_connection()
# 第三步：获取游标对象
cursor = conn.cursor()
# 第四步：具体操作
cursor.execute('select * from t1;')
# 拿到全部结果
res = cursor.fetchall()
print(res)
# 比pymysql优势在，有数据库连接池
~~~

#### orm使用

- 数据库必须自己创建

- sqlachemy不支持修改字段

~~~python
import os
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
# 字段和字段属性
from sqlalchemy import (
    ForeignKey, Column, Integer, String, Text, DateTime, UniqueConstraint, Index
)
# 制造了一个类，作为所有模型类的基类(操作只管理继承Base模型类的表)
Base = declarative_base()
class UserInfo(Base):
    # mysql中主键自动建索引：聚簇索引
    # 其他键建的索引叫：辅助索引
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)  # id 主键
    name = Column(String(32), index=True, nullable=False)  # name列，索引，不可为空
    email = Column(String(32), unique=True, nullable=True)  # 唯一
    # datetime.datetime.now不能加括号，加了括号，以后永远是当前时间
    create_time = Column(DateTime, default=datetime.datetime.now)
    introduction = Column(Text, nullable=True)

    __tablename__ = 'userinfo'  # 数据库表名称，如果不写，默认以类名小写作为表的名字
    # 类似于django的 class Meta
    __table_args__ = (
        UniqueConstraint('id', 'name', name='uix_id_name'),  # 联合唯一
        Index('ix_id_name', 'name', 'email'),  # 索引
    )
# 创建表
def create_table():
    # 创建engine对象
    engine = create_engine(
        "mysql+pymysql://%s:%s@127.0.0.1:3306/%s?charset=utf8" % (
            'root', os.getenv('MYSQL_PASSWORD'), 'flasktest'  # 用户名，mysql密码和数据库名
        ),
        max_overflow=0,  # 超过连接池大小外最多创建的连接
        pool_size=5,  # 连接池大小
        pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
        pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
    )
    # 通过engine对象创建表
    Base.metadata.create_all(engine)
# 删除表
def drop_table():
    # 创建engine对象
    engine = create_engine(
        "mysql+pymysql://%s:%s@127.0.0.1:3306/%s?charset=utf8" % (
            'root', os.getenv('MYSQL_PASSWORD'), 'flasktest'  # 用户名，mysql密码和数据库名
        ),
        max_overflow=0,  # 超过连接池大小外最多创建的连接
        pool_size=5,  # 连接池大小
        pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
        pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
    )
    # 通过engine对象删除所有表
    Base.metadata.drop_all(engine)
if __name__ == '__main__':
    create_table()
    # drop_table()
~~~

#### 线程安全

类不继承Session类，但是有该类的所有方法，如何实现（通过反射，一个个放进去）

~~~python
# 基于scoped_session实现线程安全
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from models import UserInfo
# 1 制作engine
engine = create_engine(
    "mysql+pymysql://%s:%s@127.0.0.1:3306/%s?charset=utf8" % (
        'root', os.getenv('MYSQL_PASSWORD'), 'flasktest'  # 用户名，mysql密码和数据库名
    ),
    max_overflow=0, pool_size=5, pool_timeout=30,
)
# 2 制造一个 session 类（会话）
Session = sessionmaker(bind=engine)  # 得到一个类
# 3 得到一个session对象（线程安全的session）
# 现在的session已经不是session对象了
# 为什么线程安全，还是用的local
session = scoped_session(Session)
# 4 创建一个对象
obj1 = UserInfo(name="hkw")
# 5 把对象通过add放入
session.add(obj1)
# 6 提交
session.commit()
session.close()
~~~

#### models.py

~~~python
import os
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship
# 字段和字段属性
from sqlalchemy import (
    ForeignKey, Column, Integer, String, Text, DateTime, UniqueConstraint, Index
)
# 制造了一个类，作为所有模型类的基类(操作只管理继承Base模型类的表)
Base = declarative_base()
class UserInfo(Base):
    # mysql中主键自动建索引：聚簇索引
    # 其他键建的索引叫：辅助索引
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)  # id 主键
    name = Column(String(32), index=True, nullable=False)  # name列，索引，不可为空
    email = Column(String(32), unique=True, nullable=True)  # 唯一
    # datetime.datetime.now不能加括号，加了括号，以后永远是当前时间
    create_time = Column(DateTime, default=datetime.datetime.now)
    introduction = Column(Text, nullable=True)
    __tablename__ = 'userinfo'  # 数据库表名称，如果不写，默认以类名小写作为表的名字
    # 类似于django的 class Meta
    __table_args__ = (
        UniqueConstraint('id', 'name', name='uix_id_name'),  # 联合唯一
        Index('ix_id_name', 'name', 'email'),  # 索引
    )
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
class Person(Base):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(32), index=True, nullable=False)
    # 强制写好一对多
    # 一个Hobby可以有很多人喜欢，一个人只能由一个Hobby
    hobby = Column(Integer, ForeignKey("hobby.id"))  # 默认可以为空
    # 跟数据库无关，不会新增字段，只用于快速链表操作
    # 类名，backref用于反向查询
    hobbys = relationship('Hobby', backref='hobbys')
    """hobby是整数(连接hobby的id)，hobbys是对象(跨表)"""
    __tablename__ = 'person'
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
class Hobby(Base):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(64), index=True, nullable=False, default='编程')
    __tablename__ = 'hobby'
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
# 多对多关系(实实在在存在的表)
class Boy2Girl(Base):
    __tablename__ = 'boy2girl'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    girl_id = Column(Integer, ForeignKey('girl.id'))
    boy_id = Column(Integer, ForeignKey('boy.id'))
class Girl(Base):
    __tablename__ = 'girl'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(64), unique=True, nullable=False)
class Boy(Base):
    __tablename__ = 'boy'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(64), unique=True, nullable=False)
    # 与生成表结构无关，仅用于查询方便,放在哪个单表中都可以
    # secondary 通过哪个表建关联，跟django中的through一模一样
    girls = relationship('Girl', secondary='boy2girl', backref='boys')
def create_table():
    # 创建engine对象
    engine = create_engine(
        "mysql+pymysql://%s:%s@127.0.0.1:3306/%s?charset=utf8" % (
            'root', os.getenv('MYSQL_PASSWORD'), 'flasktest'  # 用户名，mysql密码和数据库名
        ),
        max_overflow=0,  # 超过连接池大小外最多创建的连接
        pool_size=5,  # 连接池大小
        pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
        pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
    )
    # 通过engine对象创建表
    Base.metadata.create_all(engine)
if __name__ == '__main__':
    create_table()
~~~

#### 基本增删查改

- filter_by和filter的区别
  - filter_by(name='hkw')，filter_by传的是参数
  - filter(UserInfo.id>=2)，filter传的是表达式

~~~python
import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session

from models import UserInfo, Person, Hobby

engine = create_engine(
    "mysql+pymysql://%s:%s@127.0.0.1:3306/%s?charset=utf8" % (
        'root', os.getenv('MYSQL_PASSWORD'), 'flasktest'  # 用户名，mysql密码和数据库名
    ),
    max_overflow=0, pool_size=5, pool_timeout=30,
)
Session = sessionmaker(engine)
session = scoped_session(Session)
# session = Session()

# 1.新增多个对象
# obj = UserInfo(name='张三')
# obj2 = UserInfo(name='里斯')
# obj3 = UserInfo(name='王五')
# 新增同样对象
# session.add_all([
#   obj, obj2, obj3
# ])
# 新增不同对象
# session.add_all([
#     Person(name='lin', hobby=3), Hobby(name='篮球')
# ])
# 2.简单删除（查到删除）
# session.query(UserInfo).filter_by(name='hkw').delete()
# session.query(UserInfo).filter(UserInfo.id>=3).delete()
# 3.修改
# session.query(UserInfo).filter_by(id=2).update({UserInfo.name:'老王'})
# session.query(UserInfo).filter_by(id=6).update({'name':'小刘'})
# 高级修改
# session.query(UserInfo).filter(UserInfo.id > 0).update(
#     {UserInfo.name: UserInfo.name + "777"}, synchronize_session=False
# )  # 如果要把它转成字符串相加
# session.query(UserInfo).filter(UserInfo.id > 0).update(
#     {"age": UserInfo.age + 1}, synchronize_session="evaluate"
# )  # 如果要把它转成数字相加

# 4.基本查询操作
# res=session.query(UserInfo).all()
# print(res)
# res=session.query(UserInfo).first()
# print(res)

# filter传的是表达式，filter_by传的是参数
# res=session.query(UserInfo).filter(UserInfo.id>=2).all()
# print(res)
# res=session.query(UserInfo).filter_by(name='hkw').all()
# print(res)

# 了解(自定义SQL语句)
# res = session.query(UserInfo).from_statement(
#     text("SELECT * FROM UserInfo where name=:name")
# ).params(name='hkw').all()
# print(res)

session.commit()
# 并没有真正关闭连接，而是放回池中
session.close()
~~~

#### 高级操作

~~~python
import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import and_, or_
from sqlalchemy.sql import func  # 分组
from models import UserInfo, Person, Hobby

engine = create_engine(
    "mysql+pymysql://%s:%s@127.0.0.1:3306/%s?charset=utf8" % (
        'root', os.getenv('MYSQL_PASSWORD'), 'flasktest'  # 用户名，mysql密码和数据库名
    ),
    max_overflow=0, pool_size=5, pool_timeout=30,
)
Session = sessionmaker(engine)
session = scoped_session(Session)
# session = Session()

# 1 查询名字为hkw的所有UserInfo对象
# res = session.query(UserInfo).filter_by(name='hkw').all()
# print(res)
# 2 表达式，and条件连接
# res = session.query(UserInfo).filter(UserInfo.id > 1, UserInfo.name == 'hkw').all()
# print(res)
# 查找id在1和10之间，并且name=hkw的对象
# res = session.query(UserInfo).filter(UserInfo.id.between(1, 10), UserInfo.name == 'hkw').all()
# print(res)
# in条件(class_,因为这是关键字，不能直接用)
# res = session.query(UserInfo).filter(UserInfo.id.in_([2, 3, 9])).all()
# print(res)
# 取反 ~
# res = session.query(UserInfo).filter(~UserInfo.id.in_([2, 3, 9])).all()
# print(res)
# 二次筛选
# select * ...
# res = session.query(Person).filter(Person.hobby.in_(session.query(Hobby.id).filter(Hobby.name=='编程'))).all()
# print(res)
# select id,name ...
# res = session.query(Person.id, Person.name).filter(
#     Person.hobby.in_(session.query(Hobby.id).filter(Hobby.name == '编程'))
# ).all()
# print(res)

# or_包裹的都是or条件，and_包裹的都是and条件
# 查询id>3并且name=hkw的人
# res = session.query(UserInfo).filter(and_(UserInfo.id > 3, UserInfo.name == 'hkw')).all()
# print(res)
# 查询id小于等于3或者name=hkw的数据
# res = session.query(UserInfo).filter(or_(UserInfo.id <= 3, UserInfo.name == 'hkw')).all()
# print(res)
# 查询 name=hkw并且id大于3 或者 id小于等于3的数据
# res = session.query(UserInfo).filter(
#     or_(
#         UserInfo.id <= 3,
#         and_(UserInfo.name == 'hkw', UserInfo.id > 3)
#     )).all()
# print(res)

# 通配符，以h开头，不以h开头
# res = session.query(UserInfo).filter(UserInfo.name.like('h%')).all()
# print(res)
# res = session.query(UserInfo).filter(~UserInfo.name.like('h%')).all()
# print(res)

# 排序，根据name降序排列（从大到小）
# res = session.query(UserInfo).order_by(UserInfo.name.desc()).all()
# print(res)
# res = session.query(UserInfo).order_by(UserInfo.name.asc()).all()
# print(res)
# 第一个条件降序排序后，再按第二个条件升序排
# res = session.query(UserInfo.id, UserInfo.name).order_by(UserInfo.name.desc(), UserInfo.id.asc()).all()
# print(res)

# 分组
# from sqlalchemy.sql import func
# sql分组之后，要查询的字段中只能有分组字段和聚合函数
# res = session.query(UserInfo.introduction, func.count(UserInfo.name)).group_by(UserInfo.introduction).all()
# print(res)
"""
from userinfo.introduction, count(userinfo.name) from userinfo group by userinfo.introduction
"""

# haviing筛选
# res = session.query(
#     UserInfo.introduction, func.count(UserInfo.id)
# ).group_by(
#     UserInfo.introduction
# ).having(
#     func.count(UserInfo.id) > 2
# ).all()
# print(res)
"""
from userinfo.introduction, count(userinfo.id) from userinfo group by userinfo.introduction having count(userinfo.id)>2
"""

session.commit()
session.close()
~~~

#### 多表操作

~~~python
import os

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

from models import UserInfo, Person, Hobby, Boy, Girl, Boy2Girl

engine = create_engine(
    "mysql+pymysql://%s:%s@127.0.0.1:3306/%s?charset=utf8" % (
        'root', os.getenv('MYSQL_PASSWORD'), 'flasktest'  # 用户名，mysql密码和数据库名
    ),
    max_overflow=0, pool_size=5, pool_timeout=30,
)
Session = sessionmaker(bind=engine)
session = scoped_session(Session)
# session = Session()

# 1 一对多插入数据
# obj = Hobby(name='钢琴')
# session.add(obj)
# session.commit()
# p = Person(name='张三', hobby=1)
# session.add(p)
# session.commit()
# 2 方式二(默认情况不能传对象)
# 传对象Person表中要加 hobbys = relationship('Hobby', backref='hobbys')
# p = Person(name='小李', hobbys=Hobby(name='美女'))
# session.add(p)
# 等同于
# p=Person(name='hzh')
# p.hobbys=Hobby(name='泡椒')
# session.add(p)
# 3 方式三，通过反向操作
# hb = Hobby(name='旅游')
# hb.hobbys = [Person(name='lll'), Person(name='hhh')]
# session.add(hb)

# 4 查询（查询：基于连表的查询，基于对象的跨表查询）
# 4.1 基于对象的跨表查询(子查询，两次查询)
# 正查
# p = session.query(Person).filter_by(name='hkw').first()
# print(p)
# print(p.hobbys.name)
# 反查
# h = session.query(Hobby).filter_by(name='旅游').first()
# print(h.hobbys)

# 4.2 基于连表的跨表查（查一次）
"""
# 默认根据外键连表
# isouter=True 左外连，表示Person left join Hobby，没有右连接，反过来即可
# 不写是inner join
"""
# select * from person left join hobby on person.hobby=hobby.id
# person_list = session.query(Person, Hobby).join(Hobby, isouter=True)
# print(person_list)
# for row in person_list:
#     print(row[0].name, row[1].name)
# 等同于
# select * from person, hobby where person.hobby=hobby.id
# ret = session.query(Person, Hobby).filter(Person.hobby == Hobby.id)
# print(ret)

# join表，默认是inner join
# ret = session.query(Person).join(Hobby)
# print(ret)
# ret = session.query(Hobby).join(Person, isouter=True)
# print(ret)

# 指定连表字段（了解，用不到）
# ret = session.query(Person).join(Hobby, Person.id == Hobby.id, isouter=True)
# print(ret)

# 组合（了解）UNION 操作符用于合并两个或多个 SELECT 语句的结果集
# union和union all的区别(union去重，union all只管拼接到一起)
# res = session.query(UserInfo.name).filter(UserInfo.id > 2).all()
# print(res)
# res = session.query(UserInfo.name).filter(UserInfo.id < 8).all()
# print(res)
"""
[('小刘777',), ('王五777',), ('hkw',), ('jon',), ('6ge',), ('hkw',)]
[('老王777',), ('小刘777',), ('王五777',)]
"""
# q1 = session.query(UserInfo.id, UserInfo.name).filter(UserInfo.id > 2)
# q2 = session.query(UserInfo.id, UserInfo.name).filter(UserInfo.id < 8)
# ret = q1.union_all(q2).all()
# ret1 = q1.union(q2).all()
# print(ret)
# print(ret1)
"""
[(6, '小刘777'), (7, '王五777'), (8, 'hkw'), (9, 'jon'), (10, '6ge'), (11, 'hkw'), (2, '老王777'), (6, '小刘777'), (7, '王五777')]
[(6, '小刘777'), (7, '王五777'), (8, 'hkw'), (9, 'jon'), (10, '6ge'), (11, 'hkw'), (2, '老王777')]
"""

# 多对多
# session.add_all([
#     Boy(name='霍建华'),
#     Boy(name='胡歌'),
#     Girl(name='刘亦菲'),
#     Girl(name='林心如'),
# ])
# session.commit()
# session.add_all([
#     Boy2Girl(girl_id=1, boy_id=1),
#     Boy2Girl(girl_id=2, boy_id=1)
# ])
# session.commit()

# 要有字段girls = relationship('Girl', secondary='boy2girl', backref='boys')
# girl = Girl(name='章若楠')
# girl.boys = [Boy(name='周杰伦'), Boy(name='张杰')]
# session.add(girl)
# session.commit()
# boy = Boy(name='ai坤')
# boy.girls = [Girl(name='谢娜'), Girl(name='王欣雨')]
# session.add(boy)
# session.commit()

# 基于对象的跨表查
# girl = session.query(Girl).filter_by(id=3).first()
# print(girl.boys)

# 基于连表的跨表查询
# 查询胡歌约过的所有妹子
# select girl.name from girl,boy,boy2girl where girl.id=boy2girl.boy_id,boy.id=boy2girl.girl_id and boy.name='胡歌'
# ret = session.query(Girl.name).filter(
#     Boy.id == Boy2Girl.boy_id, Girl.id == Boy2Girl.girl_id, Boy.name == '胡歌'
# ).all()
# print(ret)
"""
# select girl.name from girl 
    # inner join boy2girl on girl.id=boy2girl.girl_id 
    # inner join boy on boy.id=boy2girl.boy_id
    # where boy.name='胡歌'
"""
# ret=session.query(Girl.name).join(Boy2Girl).join(Boy).filter(Boy.name=='胡歌')
# print(ret)
# ret = session.query(Girl.name).join(Boy2Girl).join(Boy).filter_by(name='胡歌')
# print(ret)

# 执行原生sql
# django中orm如何执行原生sql(models.UserInfo.objects.row)
# from sqlalchemy.sql import text
# with engine.connect() as conn:
#     cursor = session.execute(text('select name from userinfo where name=:name'), params={'name': 'hkw'})
#     print(cursor)
#     print(cursor.first())

session.commit()
session.close()
~~~

## Flask-SQLAlchemy

~~~python
# 作用：能像Django一样敲命令初始化数据库
# 安装：pip install Flask-SQLAlchemy
# 看代码：https://github.com/HkwJsxl/PythonFullStackFlask/tree/master/oldboy/Flask-SQLAlchemy_
~~~

## flask-admin

安装：`pip3 install flask_admin`

~~~python
# 目录
flask_admin_
    __init__.py
    admins.py
    manage.py
    models.py
    
# manage.py
import os
from flask import Flask
from flask_admin import Admin
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
engine = create_engine(
    "mysql+pymysql://%s:%s@127.0.0.1:3306/%s?charset=utf8" % (
        'root', os.getenv('MYSQL_PASSWORD'), 'flasktest'  # 用户名，mysql密码和数据库名
    ),
    max_overflow=0, pool_size=5, pool_timeout=30,
)
Session = sessionmaker(bind=engine)
session = scoped_session(Session)
app = Flask(__name__)
# 将app注册到admin中
admin = Admin(app)
if __name__ == "mian":
    app.run()
    # 访问127.0.0.1:5000/admin端口，会得到一个空白的页面
    
# models.py
import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    ForeignKey, Column, Integer, String, Text, DateTime, UniqueConstraint, Index
)
Base = declarative_base()
class UserInfo(Base):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(32), index=True, nullable=False)
    email = Column(String(32), unique=True, nullable=True)
    create_time = Column(DateTime, default=datetime.datetime.now)
    introduction = Column(Text, nullable=True)
    __tablename__ = 'userinfo'
    __table_args__ = (
        UniqueConstraint('id', 'name', name='uix_id_name'),
        Index('ix_id_name', 'name', 'email'),  # 索引
    )
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    
# admin.py
import os
from .manage import admin, session
# 在将表注册之前应该对app进行配置
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@127.0.0.1:3307/py9api?charset=utf8mb4"
SQLALCHEMY_POOL_SIZE = 5
SQLALCHEMY_POOL_TIMEOUT = 30
SQLALCHEMY_POOL_RECYCLE = -1
# 导入models文件的中的表模型
from flask_admin.contrib.sqla import ModelView
from models import UserInfo
admin.add_view(ModelView(UserInfo, session))
"""如果有个字段是图片字段"""
# 配置上传文件的路径
from flask_admin.contrib.fileadmin import FileAdmin, form
file_path = os.path.join(os.path.dirname(__file__), 'static')
admin.add_view(FileAdmin(file_path, '/static/', name='上传文件'))
# 如果有个字段要是上传文件重写该方法的modleView类，假设imgae_url是文件图片的字段
class ImagesView(ModelView):
    form_extra_fields = {
        'image_url': form.ImageUploadField('Image',
                                           base_path=file_path,
                                           relative_path='uploadFile/'
                                           )
    }
# admin.add_view(ImagesView(Images, session))
~~~

# 问题

## Flask如何记录日志

~~~python
Flask自带了记录日志的功能，直接app.loger
~~~

# 报错解决

> `AttributeError: 'tuple' object has no attribute 'drivername'`

复制粘贴时，手误多了一个逗号，所以导致报错

![image-20230223170231759](https://img2023.cnblogs.com/blog/2570053/202302/2570053-20230223170233256-1491266760.png)

> 安装`flask_migrate`包内没有`MigrateCommand`

`from flask_migrate import Migrate, MigrateCommand`

原因是`flask_migrate`高版本不再支持`MigrateCommand`，降低版本即可

`pip install flask_migrate==2.7.0`


