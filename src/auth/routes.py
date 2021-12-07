from flask import Blueprint, request, render_template, session, current_app

from src.access import group_permission_validation_decorator
from src.useMySql import getDataFromDataBase

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login', methods=['GET', 'POST'])
@group_permission_validation_decorator
def login():
    """
    Функция отображает форму авторизации и при вводе
    входных данных авторизирует пользователя в системе, путем
    добавления роли в сессию
    :return: Template
    """
    if request.method == 'GET':
        return render_template('auth/login.html')

    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        message = 'Неправильные логин или пароль'
        data = getDataFromDataBase('login.sql', login=login, password=password)
        if data['result'] is not None:
            if session.get('sessionID') is None:
                session['sessionID'] = data['result'][0]['role']
                message = 'Добро пожаловать'
            else:
                message = 'Вы уже авторизированы'

        return render_template('info.html', message=message)

