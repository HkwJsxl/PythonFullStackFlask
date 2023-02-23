from flask import Blueprint

account = Blueprint('user', __name__, url_prefix='/user', template_folder='templates')


# http://127.0.0.1:5000/user/
@account.route('/', methods=['GET'])
def index():
    return 'index'
