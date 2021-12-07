import datetime

from flask import Blueprint, render_template, request, session

from src.access import group_permission_validation_decorator
from src.useMySql import getDataFromDataBase, execute

basketHandler = Blueprint('basketHandler', __name__, template_folder='templates')


@basketHandler.route('/', methods=['GET', 'POST'])
@group_permission_validation_decorator
def enter():
    if request.method == 'GET':
        return render_template('basket/enter.html')

    id = request.form.get('id')
    start_date = request.form.get('start_date')
    start_date = start_date if start_date else datetime.date.today()

    data = getDataFromDataBase('checkArendator.sql', id=id)

    if data['result'] is None:
        return render_template('info.html',
                               message='Не удалось начать оформление заказа: ID арендатора не действителен')

    order_data = getDataFromDataBase('getOrder.sql', start_date=start_date, arend_id=id)['result']

    billboards_in_order = []
    if order_data is not None:
        order_data = order_data[0]
        billboards_in_order = getDataFromDataBase('getOrderBillboards.sql', id=order_data.get('ID'))['result']
        if billboards_in_order is None:
            billboards_in_order = []
    else:
        order_data = {
            'start_date': start_date,
            'arend_id': id
        }

    billboards = []
    all_billboards = getDataFromDataBase('getAllBillboards.sql')['result']

    if all_billboards is None:
        all_billboards = []

    for bill in all_billboards:
        id = bill.get('ID')
        is_include = False

        for b in billboards_in_order:
            if b.get('ID') == id:
                is_include = True
                break

        if not is_include:
            billboards.append(bill)

    session['in_basket'] = billboards_in_order
    session['out_basket'] = billboards
    session['order_data'] = order_data

    return render_template('basket/basket.html', all_billboards=session['out_basket'],
                           billboards_in_order=session['in_basket'], order_data=session['order_data'])


@basketHandler.route('/add-billboard', methods=['POST'])
@group_permission_validation_decorator
def add_billboard():
    id = int(request.form.get('id'))

    return render_template('basket/add.html', id=id)


@basketHandler.route('/select', methods=['POST'])
@group_permission_validation_decorator
def select():
    id = int(request.form.get('id'))
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    if start_date < session.get('order_data').get('start_date'):
        return render_template('basket/add.html', id=id,
                               start=start_date,
                               end=end_date,
                               mes="Начальная дата не может быть раньше даты оформления заказа")

    if start_date >= end_date:
        return render_template('basket/add.html', id=id,
                               start=start_date,
                               end=end_date,
                               mes="Начальная дата должна быть строго раньше конечной")

    isNotFree = getDataFromDataBase('checkAvailabilityBilboard.sql',
                                 id=id,
                                 start_date=start_date,
                                 end_date=end_date)['result']

    if isNotFree:
        return render_template('basket/add.html', id=id,
                               start=start_date,
                               end=end_date,
                               mes="Билборд не доступен в это время")

    selected_billboard = {}
    out = session['out_basket']
    new_out = []
    for billboard in out:
        if billboard.get('ID') != id:
            new_out.append(billboard)
        else:
            selected_billboard = billboard

    session['out_basket'] = new_out
    selected_billboard['start_date'] = start_date
    selected_billboard['end_date'] = end_date

    in_basket = session['in_basket']
    in_basket.append(selected_billboard)
    session['in_basket'] = in_basket

    return render_template('basket/basket.html', all_billboards=session['out_basket'],
                           billboards_in_order=session['in_basket'], order_data=session['order_data'])


@basketHandler.route('/cancel', methods=['POST'])
@group_permission_validation_decorator
def cancel():
    id = int(request.form.get('id'))

    selected_billboard = {}
    in_basket = session['in_basket']
    new_in_basket = []
    for billboard in in_basket:
        if billboard.get('ID') != id:
            new_in_basket.append(billboard)
        else:
            selected_billboard = billboard

    session['in_basket'] = new_in_basket

    out = session['out_basket']
    out.append(selected_billboard)
    session['out_basket'] = out

    return render_template('basket/basket.html', all_billboards=session['out_basket'],
                           billboards_in_order=session['in_basket'], order_data=session['order_data'])


@basketHandler.route('/clear', methods=['POST'])
@group_permission_validation_decorator
def clear():
    in_basket = session['in_basket']
    out = session['out_basket']

    for bill in in_basket:
        out.append(bill)

    session['in_basket'] = []
    session['out_basket'] = out

    return render_template('basket/basket.html', all_billboards=session['out_basket'],
                           billboards_in_order=session['in_basket'], order_data=session['order_data'])


@basketHandler.route('/send', methods=['POST'])
@group_permission_validation_decorator
def send():
    in_basket = session['in_basket']
    order_data = session['order_data']

    full_cost = 0
    for bill in in_basket:
        days = get_days(bill['start_date'], bill['end_date'])
        full_cost += bill.get('Цена') * days

    if order_data.get('ID'):
        execute('updateOrder.sql', full_cost=full_cost, id=order_data.get('ID'))
    else:
        execute('insertOrder.sql',
                full_cost=full_cost,
                id=order_data.get('arend_id'),
                start_date=order_data.get('start_date')
                )

        order_data['ID'] = getDataFromDataBase('getOrder.sql',
                                               start_date=order_data.get('start_date'),
                                               arend_id=order_data.get('arend_id'))['result'][0].get('ID')

    execute('deleteOrdersStr.sql',
            id=order_data.get('ID'),
            )

    for bill in in_basket:
        days = get_days(bill['start_date'], bill['end_date'])

        execute('insertOrderBillboards.sql',
                id=order_data.get('ID'),
                start_ar=bill.get('start_date'),
                end_ar=bill.get('end_date'),
                cost_period=bill.get('Цена') * days,
                bil_id=bill.get('ID'),
                )

    return render_template('info.html', message='Заказ успешно оформлен')


def get_days(start_date, end_date):
    a = start_date.split('-')
    b = end_date.split('-')
    start_date = datetime.date(int(a[0]), int(a[1]), int(a[2]))
    end_date = datetime.date(int(b[0]), int(b[1]), int(b[2]))
    return (end_date - start_date).days
