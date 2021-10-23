import json

from flask import Blueprint, request, render_template

from access import group_validation_decorator, group_permission_validation_decorator
from useMySql.sqlProvider import SQLProvider

dbHandler = Blueprint('dbHandler', __name__, template_folder='templates')

config = [
    {
        'name': 'Показать всех клиентов, которые не подключали новых услуг в заданный диапазон дат.',
        'url': '/db/all-clients-not-connect-for-period'
    },
    {
        'name': 'Показать все услуги, цена которых выше заданного значения.',
        'url': '/db/all-services-where-price-bigger'
    }
]

dbConfig = json.load(open('configs/db.json'))

provider = SQLProvider('./dbHandler/sql', dbConfig)


@dbHandler.route('/')
def menu():
    return render_template('dbHandler/menu.html', querys=config)


@dbHandler.route('/all-clients-not-connect-for-period', methods=["GET", "POST"])
@group_validation_decorator
@group_permission_validation_decorator
def allClientsNotConnectForPeriod():
    if request.method == "GET":
        return render_template('dbHandler/dateUser.html', description=config[0].get('name'))
    if request.method == "POST":
        before = request.form.get('before')
        after = request.form.get('after')

        sql = provider.get('dateUser.sql', before=before, after=after)
        data = provider.exec(sql)
        return render_template('dbHandler/dateUser.html', description=config[0].get('name'), isResponse=True, data=data, vb=before, va=after)


@dbHandler.route('/all-services-where-price-bigger', methods=["GET", "POST"])
@group_validation_decorator
@group_permission_validation_decorator
def allServicesWherePriceBigger():
    if request.method == "GET":
        return render_template('dbHandler/servicePriceBigger.html', description=config[1].get('name'))
    price = int(request.form.get('price'))
    sql = provider.get('servicePriceBigger.sql', price=price)
    data = provider.exec(sql)
    return render_template('dbHandler/servicePriceBigger.html', description=config[0].get('name'), isResponse=True, data=data, vp=price)
