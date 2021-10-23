from functools import wraps

from flask import session, current_app, request


def group_validation():
    return bool(session.get('group'))


def group_validation_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if group_validation():
            return func(*args, **kwargs)
        return 'Permission denied'

    return wrapper


def group_permission_validation():
    access_config = current_app.config['ACCESS']
    group = session.get('group', 'unauthorized')

    url = request.endpoint.split('.')
    target_app = '' if len(url) == 1 else url[0]

    return group in access_config and target_app in access_config[group]


def group_permission_validation_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if group_permission_validation():
            return func(*args, **kwargs)
        return 'Permission denied'

    return wrapper
