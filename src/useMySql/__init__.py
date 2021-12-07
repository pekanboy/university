import json
from src.useMySql.sqlProvider import SQLProvider

dbConfig = json.load(open('configs/db.json'))
provider = SQLProvider('useMySql/sql', dbConfig)


def getDataFromDataBase(file, **kwargs):
    """
    Функция для получения данных из БД
    :param file: Имя файла с запросом
    :param kwargs: Аргументы запроса
    :return: Полученные данные
    """
    sql = provider.get(file, **kwargs)
    data = provider.exec(sql)

    if data is None:
        data = {'schema': [], 'result': []}

    if len(data['result']) == 0:
        data['result'] = None

    return data


def execute(file, **kwargs):
    """
    Функция для выполнения запросов в БД
    без получения результата
    :param file: Имя файла с запросом
    :param kwargs: Аргументы запроса
    :return: boolean: Запрос прошел успешно или нет
    """
    sql = provider.get(file, **kwargs)
    res = provider.execWithoutData(sql)
    return res == 1
