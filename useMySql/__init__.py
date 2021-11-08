import json

from useMySql.dbСonnection import DBConnection
from useMySql.sqlProvider import SQLProvider

dbConfig = json.load(open('configs/db.json'))
provider = SQLProvider('./queryHandler/sql', dbConfig)


def getDataFromDataBase(file, **kwargs):
    sql = provider.get(file, **kwargs)
    data = provider.execWithData(sql)

    if len(data['result']) == 0:
        data['result'] = None

    return data


def execute(file, **kwargs):
    sql = provider.get(file, **kwargs)
    res = provider.execWithoutData(sql)
    return res == 1
