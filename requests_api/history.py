from typing import List, Any


def out_history(response_database_in: Any, user_id_in: str) -> List:
    """
    Функция выводящая список последних 5 запросов пользователя из базы данных
    :param response_database_in: результат запроса к базе данных
    :param user_id_in: id пользователя
    :return: список результатов запросов
    """
    count = 1
    out_total = []
    if len(response_database_in) > 5:
        response_database_in = response_database_in[:5]
    for element in response_database_in:
        if element.user_id == user_id_in:
            out_total.append(
                f'{element.created_request}\n'
                f'  {count} запрос:  \n  '
                f' {element.request}'
            )
            count += 1
    return out_total
