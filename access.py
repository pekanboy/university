from functools import wraps
from flask import session, current_app, request, render_template


def group_permission_validation():
    access_config = current_app.config['ACCESS']
    group = session.get('sessionID', 'unauthorized')

    url = request.endpoint.split('.')

    target_app = url[0]
    target_method = url[1]

    return group in access_config \
           and target_app in access_config[group] \
           and target_method in access_config[group][target_app]


def group_permission_validation_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if group_permission_validation():
            return func(*args, **kwargs)
        return render_template('info.html', message='Отказано в доступе')

    return wrapper
