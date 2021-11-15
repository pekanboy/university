import json
from src.useMySql.sqlProvider import SQLProvider

dbConfig = json.load(open('src/configs/db.json'))
provider = SQLProvider('src/queryHandler/sql', dbConfig)


def getDataFromDataBase(file, **kwargs):
    sql = provider.get(file, **kwargs)
    data = provider.exec(sql)

    if len(data['result']) == 0:
        data['result'] = None

    return data


def execute(file, **kwargs):
    sql = provider.get(file, **kwargs)
    res = provider.execWithoutData(sql)
    return res == 1
