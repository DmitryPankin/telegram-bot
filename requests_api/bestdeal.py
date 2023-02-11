from requests_api import params_requests


def change_params_commands_best():
    """
    Функция изменяет параметры запроса API для команды bestdeal

    """
    params_requests.command = params_requests.commands[1]
    params_requests.payload_1["sort"] = params_requests.params_sort[1]
    params_requests.payload_1["filters"] = params_requests.filters


if __name__ == '__main__':
    change_params_commands_best()
