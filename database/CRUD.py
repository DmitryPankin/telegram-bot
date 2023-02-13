from typing import Any, List
from database import models


def _store_data(database: models.db, model: models.History, data: List) -> None:
    """Запись результата поиска в базу данных"""
    with database.atomic():
        model.insert_many(data).execute()


def _retrieve_data(database: models.db, model: models.db, *column: Any) -> Any:
    """Чтение результата поиска из базы данных"""
    with database.atomic():
        response = model.select(*column)
    return response


class Interface:
    @staticmethod
    def create():
        return _store_data

    @staticmethod
    def retrieve():
        return _retrieve_data


if __name__ == '__main__':
    Interface()
