from flask import Flask
from oldboy.blueprint.views import user

app = Flask(__name__)

app.register_blueprint(user.account)

if __name__ == '__main__':
    app.run()
