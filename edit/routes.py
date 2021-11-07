from flask import Blueprint, render_template

from access import group_permission_validation_decorator

editHandler = Blueprint('editHandler', __name__, template_folder='templates')

config = [
    {
        'name': 'Билборды',
        'url': '/edit/'
    },
]


@editHandler.route('/')
@group_permission_validation_decorator
def menu():
    return render_template('editHandler/menu.html', data_bases=config)

