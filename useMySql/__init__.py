import json
from useMySql.sqlProvider import SQLProvider

dbConfig = json.load(open('configs/db.json'))
provider = SQLProvider('./queryHandler/sql', dbConfig)


def getDataFromDataBase(file, **kwargs):
    sql = provider.get(file, **kwargs)
    data = provider.exec(sql)

    if len(data['result']) == 0:
        data['result'] = None

    return data
