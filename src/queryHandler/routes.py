from flask import Blueprint, request, render_template

from src.access import group_permission_validation_decorator
from src.useMySql import getDataFromDataBase

queryHandler = Blueprint('queryHandler', __name__, template_folder='templates')

config = [
    {
        'name': 'Показать все сведения об арендаторах, заключивших договора в заданную дату',
        'url': '/db/arendator-for-date'
    },
    {
        'name': 'Показать всех арендаторов, телефоны которых имеют заданный префикс',
        'url': '/db/arendator-for-prefix-telephone'
    },
{
        'name': 'Показать данные о билбордах, имеющих заданную стоимость аренды билборода в день',
        'url': '/db/billboards-for-cost'
    }
]


@queryHandler.route('/')
@group_permission_validation_decorator
def menu():
    return render_template('queryHandler/menu.html', querys=config)


@queryHandler.route('/arendator-for-date', methods=["GET", "POST"])
@group_permission_validation_decorator
def arendatorForDate():
    if request.method == "GET":
        return render_template('queryHandler/arendatorForDate.html', description=config[0].get('name'))
    if request.method == "POST":
        date = request.form.get('date')
        data = getDataFromDataBase('arendatorForDate.sql', date=date)
        return render_template('queryHandler/response.html', schema=data['schema'], result=data['result'])


@queryHandler.route('/arendator-for-prefix-telephone', methods=["GET", "POST"])
@group_permission_validation_decorator
def arendatorForPrefixTelephone():
    if request.method == "GET":
        return render_template('queryHandler/arendatorForPrefixTelephone.html', description=config[1].get('name'))
    if request.method == "POST":
        prefix = request.form.get('prefix')
        data = getDataFromDataBase('arendatorForPrefixTelephone.sql', prefix=prefix)
        return render_template('queryHandler/response.html', schema=data['schema'], result=data['result'])


@queryHandler.route('/billboards-for-cost', methods=["GET", "POST"])
@group_permission_validation_decorator
def billboardsForCost():
    if request.method == "GET":
        return render_template('queryHandler/billboardsForCost.html', description=config[2].get('name'))
    if request.method == "POST":
        cost = request.form.get('cost')
        data = getDataFromDataBase('billboardsForCost.sql', cost=cost)
        return render_template('queryHandler/response.html', schema=data['schema'], result=data['result'])