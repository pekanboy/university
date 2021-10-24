from flask import Blueprint, request, render_template

from access import group_permission_validation_decorator
from useMySql import getDataFromDataBase

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


@dbHandler.route('/')
@group_permission_validation_decorator
def menu():
    return render_template('dbHandler/menu.html', querys=config)


@dbHandler.route('/all-clients-not-connect-for-period', methods=["GET", "POST"])
@group_permission_validation_decorator
def allClientsNotConnectForPeriod():
    if request.method == "GET":
        return render_template('dbHandler/dateUser.html', description=config[0].get('name'))

    before = request.form.get('before')
    after = request.form.get('after')

    data = getDataFromDataBase('dateUser.sql', before=before, after=after)
    return render_template('dbHandler/response.html', schema=data['schema'], result=data['result'])


@dbHandler.route('/all-services-where-price-bigger', methods=["GET", "POST"])
@group_permission_validation_decorator
def allServicesWherePriceBigger():
    if request.method == "GET":
        return render_template('dbHandler/servicePriceBigger.html', description=config[1].get('name'))

    price = int(request.form.get('price'))
    data = getDataFromDataBase('servicePriceBigger.sql', price=price)
    return render_template('dbHandler/response.html', schema=data['schema'], result=data['result'])
