from flask import Blueprint, request, render_template

from dbHandler.useMySql.sqlProvider import SQLProvider

dbHandler = Blueprint('dbHandler', __name__, template_folder='templates')

config = [
    {
        'name': 'Показать все сведения об арендаторах, заключивших договора в заданную дату',
        'url': '/query/request1'
    }
]

dbConfig = {
  "host": "localhost",
  "port": 3306,
  "user": "root",
  "password": "",
  "db": "coursework"
}

provider = SQLProvider('./dbHandler/sql', dbConfig)


@dbHandler.route('/')
def menu():
    return render_template('dbHandler/menu.html', querys=config)


@dbHandler.route('/request1', methods=["GET", "POST"])
def arendatorForDate():
    if request.method == "GET":
        return render_template('dbHandler/dateUser.html', description=config[0].get('name'))
    if request.method == "POST":
        date = request.form.get('date')

        sql = provider.get('dateUser.sql', date=date)
        data = provider.exec(sql)
        if len(data['result']) == 0:
            data['result'] = None
        return render_template('dbHandler/response.html', schema=data['schema'], result=data['result'])
