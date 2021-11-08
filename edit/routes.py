import json

from flask import Blueprint, render_template, request, redirect, url_for

from access import group_permission_validation_decorator
from useMySql import getDataFromDataBase, execute

editHandler = Blueprint('editHandler', __name__, template_folder='templates')

config = [
    {
        'name': 'Услуги',
        'url': '/edit/services'
    },
]


@editHandler.route('/')
@group_permission_validation_decorator
def menu():
    return render_template('editHandler/menu.html', data_bases=config)


@editHandler.route('/services', methods=['GET', 'POST'])
@group_permission_validation_decorator
def services():
    if request.method == "GET":
        data = getDataFromDataBase('getAllServices.sql')
        return render_template('editHandler/services.html', schema=data['schema'], result=data['result'])

    if request.method == 'POST':
        data = json.loads(request.data)
        if data['type'] == 'delete':
            res = execute('deleteService.sql', id=data['id'])
            if res:
                return 'Success', 200
            return 'InternalServerError', 500


@editHandler.route('/services-add', methods=['GET', 'POST'])
@group_permission_validation_decorator
def add():
    if request.method == 'GET':
        return render_template('editHandler/add.html')
    if request.method == 'POST':
        execute('addService.sql', name=request.form.get('name'), price=request.form.get('price'))
        return redirect('/edit/services')


@editHandler.route('/services-change', methods=['GET', 'POST'])
@group_permission_validation_decorator
def change():
    id = request.args.get('id')
    price = request.args.get('price')
    name = request.args.get('name')
    if request.method == 'GET':
        return render_template('editHandler/change.html', price=price, name=name, id=id)
    if request.method == 'POST':
        execute('changeService.sql', id=id, name=request.form.get('name'), price=request.form.get('price'))
        return redirect('/edit/services')

