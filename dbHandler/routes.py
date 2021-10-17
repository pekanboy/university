from flask import Blueprint, request, render_template

from useMySql.sqlProvider import SQLProvider

dbHandler = Blueprint('dbHandler', __name__, template_folder='templates')

config = [
    {
        'name': 'Показать всех клиентов, которые не подключали новых услуг в заданный диапазон дат.',
        'url': '/db/all-clients-not-connect-for-period'
    }
]

dbConfig = {
  "host": "localhost",
  "port": 3306,
  "user": "root",
  "password": "",
  "db": "university"
}

provider = SQLProvider('./dbHandler/sql', dbConfig)


@dbHandler.route('/')
def menu():
    return render_template('dbHandler/menu.html', querys=config)


@dbHandler.route('/all-clients-not-connect-for-period', methods=["GET", "POST"])
def allClientsNotConnectForPeriod():
    if request.method == "GET":
        return render_template('dbHandler/dateUser.html', description=config[0].get('name'))
    if request.method == "POST":
        before = request.form.get('before')
        after = request.form.get('after')

        sql = provider.get('dateUser.sql', before=before, after=after)
        data = provider.exec(sql)
        return render_template('dbHandler/response.html', schema=data['schema'], result=data['result'])
