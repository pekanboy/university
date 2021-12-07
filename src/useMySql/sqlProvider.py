
import os
from string import Template

from .dbСonnection import DBConnection


class SQLProvider:
    def __init__(self, file_path, config):
        """
        Инициализация переменных начальными значениями.
        Также чтение всех файлов директории и занесении их в словарь
        :param file_path: Пусть к папке со скриптами
        :param config: Сайл конфигурации
        """
        self._scripts = {}
        self._config = config

        for file in os.listdir(file_path):
            _, expression = os.path.splitext(file)
            if expression == '.sql':
                self._scripts[file] = Template(open(f'{file_path}/{file}', 'r').read())

    def get(self, file_name, **kwargs):
        """
        Получения SQL запроса в виде строки
        :param file_name: Имя файла со скриптом
        :param kwargs: Аргументы запроса
        :return: String: SQL запрос
        """
        return self._scripts[file_name].substitute(**kwargs)

    def exec(self, query):
        """
        Выполнение запроса и возвращение результата
        :param query: Запрос
        :return: Результат запроса
        """
        with DBConnection(self._config) as cursor:
            if cursor is None:
                raise ValueError('Cursor is None')
            elif cursor:
                cursor.execute(query)

                result = []
                schema = [column[0] for column in cursor.description]

                for row in cursor.fetchall():
                    result.append(dict(zip(schema, row)))
                return {
                    "schema": schema,
                    "result": result
                }

    def execWithoutData(self, query):
        """
        Выполнение запроса без результата
        :param query: Запрос
        """
        with DBConnection(self._config) as cursor:
            if cursor is None:
                raise ValueError('Cursor is None')
            return cursor.execute(query)
