from flask import Blueprint

dbHandler = Blueprint('dbHandler', __name__, template_folder='templates')


@dbHandler.route('/')
def index():
    return "dbHandler"
