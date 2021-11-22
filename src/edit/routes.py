import json

from flask import Blueprint, render_template, request, redirect

from src.access import group_permission_validation_decorator
from src.useMySql import getDataFromDataBase, execute

editHandler = Blueprint('editHandler', __name__, template_folder='templates')

config = [
    {
        'name': 'Билборды',
        'url': '/edit/billboards'
    },
]


@editHandler.route('/')
@group_permission_validation_decorator
def menu():
    return render_template('editHandler/menu.html', data_bases=config)


@editHandler.route('/billboards', methods=['GET', 'POST'])
@group_permission_validation_decorator
def billboards():
    if request.method == "GET":
        data = getDataFromDataBase('getAllBillboards.sql')
        return render_template('editHandler/billboards.html', schema=data['schema'], result=data['result'])

    if request.method == 'POST':
        data = json.loads(request.data)
        res = execute('deleteBillboard.sql', id=data['id'])
        if res:
            return 'Success', 200
        return 'InternalServerError', 500


@editHandler.route('/billboard-add', methods=['GET', 'POST'])
@group_permission_validation_decorator
def add():
    if request.method == 'GET':
        return render_template('editHandler/add.html')
    if request.method == 'POST':
        date = request.form.get('date')
        square = request.form.get('square')
        address = request.form.get('address')
        cost = request.form.get('cost')
        execute('addBillboard.sql', date=date, square=square, address=address, cost=cost)
        return redirect('/edit/billboards')




@editHandler.route('/billboard-change', methods=['GET', 'POST'])
@group_permission_validation_decorator
def change():
    id = request.args.get('id')

    if request.method == 'GET':
        date = request.args.get('date')
        square = request.args.get('square')
        address = request.args.get('address')
        cost = request.args.get('cost')
        return render_template('editHandler/change.html', id=id, date=date, square=square, address=address, cost=int(cost))
    if request.method == 'POST':
        date = request.form.get('date')
        square = request.form.get('square')
        address = request.form.get('address')
        cost = request.form.get('cost')
        execute('changeBillboard.sql', id=id, date=date, square=square, address=address, cost=cost)
        return redirect('/edit/billboards')
