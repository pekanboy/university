import json

from flask import Flask, render_template, session, current_app

from src.auth.routes import auth
from src.basket.routes import basketHandler
from src.edit.routes import editHandler
from src.queryHandler.routes import queryHandler

app = Flask(__name__)
app.register_blueprint(queryHandler, url_prefix='/db')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(editHandler, url_prefix='/edit')
app.register_blueprint(basketHandler, url_prefix='/basket')

app.config['SECRET_KEY'] = 'asdhashd32kgasd829ged'
app.config['ACCESS'] = json.load(open('configs/access.json'))


@app.route('/')
def index():
    """
    Отображение главного меню
    """
    return render_template('index.html', isAuth=bool(session.get('sessionID')))


@app.route('/exit')
def exit():
    """
    Обработчик для выхода или Информационной системы
    :return:
    """
    if session.get('sessionID'):
        session.pop('sessionID')
        return render_template('info.html', message='Спасибо, до свидания!')
    return render_template('info.html', message='Выход не выполнен, вы не авторизированы')


@app.errorhandler(404)
def notFound(e):
    return render_template('notFound.html'), 404


if __name__ == '__main__':
    app.run(host='localhost', port=8084)
