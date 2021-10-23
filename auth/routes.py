from flask import Blueprint, request, render_template, session

from access import group_permission_validation_decorator

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login', methods=['GET', 'POST'])
@group_permission_validation_decorator
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        if login == 'admin' and password == 'admin':
            session['group'] = 'admin'
            return 'OK(admin)'

        if login == 'typical' and password == 'typical':
            session['group'] = 'typical'
            return 'OK(typical)'

        return 'no login'
