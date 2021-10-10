from typing import Optional

import pymysql as pymysql
from pymysql import OperationalError


class DBConnection:
    def __init__(self, config: dict):
        self.config = config
        self.cursor = None
        self.conn = None

    def __enter__(self) -> Optional[pymysql.cursors.Cursor]:
        try:
            self.conn = pymysql.connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor
        except OperationalError as err:
            print("\033[31m {}" .format(f'Error(data base). Code: {err.args[0]}. Description: {err.args[1]}'))
            return None
        except Exception as err:
            print("\033[31m {}" .format(f'Error(any). Code: {err.args[0]}. Description: {err.args[1]}'))
            return None

    def __exit__(self, exc_type, exc_value, exc_trace):
        if exc_value:
            print("\033[31m {}" .format(f'Error(any). Code: {exc_value.args[0]}. Description: {exc_value.args[1]}'))
        if self.conn is not None and self.cursor is not None:
            self.conn.commit()
            self.conn.close()
        return True
