from flask import Flask
from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)


@app.route('/')
def index():
    return 'index'


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


if __name__ == '__main__':
    manager.run()
