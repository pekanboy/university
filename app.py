import json

from flask import Flask, render_template, session, current_app

from auth.routes import auth
from dbHandler.routes import dbHandler

app = Flask(__name__)
app.register_blueprint(dbHandler, url_prefix='/db')
app.register_blueprint(auth, url_prefix='/auth')

app.config['SECRET_KEY'] = 'asdhashd32kgasd829ged'
app.config['ACCESS'] = json.load(open('configs/access.json'))


@app.route('/')
def index():
    return render_template('index.html', isAuth=bool(session.get('sessionID')))


@app.route('/exit')
def exit():
    session.pop('sessionID')
    return render_template('info.html', message='Спасибо, до свидания!')


if __name__ == '__main__':
    app.run(host='localhost', port=8081)
