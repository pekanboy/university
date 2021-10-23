import json

from flask import Flask, render_template, session

from access import group_permission_validation_decorator
from auth.routes import auth
from dbHandler.routes import dbHandler

app = Flask(__name__)
app.register_blueprint(dbHandler, url_prefix='/db')
app.register_blueprint(auth, url_prefix='/auth')

app.config['SECRET_KEY'] = 'asdhashd32kgasd829ged'
app.config['ACCESS'] = json.load(open('configs/access.json'))


@app.route('/')
@group_permission_validation_decorator
def index():
    return render_template('index.html')


@app.route('/exit')
@group_permission_validation_decorator
def exit():
    session.clear()
    return "Спасибо, до свидания!"


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
