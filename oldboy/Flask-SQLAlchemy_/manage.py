from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from start import create_app
from start import db

app = create_app()
# flask-script的操作
manager = Manager(app)
# flask_migrate的操作，必须跟flask-script合用
Migrate(app, db)
# 相当于你写了一个db函数
# 这句是支持敲命令python manage.py db init
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
