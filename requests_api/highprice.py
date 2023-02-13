from requests_api import params_requests


def change_params_commands_high():
    """
    Функция изменяет параметры запроса API для команды highprice

    """
    params_requests.command = params_requests.commands[0]
    params_requests.payload_1["sort"] = params_requests.params_sort[0]


if __name__ == '__main__':
    change_params_commands_high()
