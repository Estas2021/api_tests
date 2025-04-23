import requests
import pprint

from json import (
    loads,
    JSONDecodeError
)


def test_post_v1_account():
    # 1 регистрация пользака

    url = 'http://5.63.153.31:5051/v1/account'

    login = 'efremov_test6'
    password = '123456789'
    email = f'{login}@mail.ru'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account', json=json_data)

    print('\n')
    print(response.status_code)
    print(response.text)

    assert response.status_code == 201, f"Пользак не был создан {response.json()}"

    # 2 Получение писем из почтового ящика

    params = {
        'limit': '50',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)

    assert response.status_code == 200, "Письма не были получены"

    # 3 Получить активационный токен
    token = None
    try:
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']

            if user_login == login:
                print('\n')
                print(user_login)
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                print(token)
    except JSONDecodeError:
        print("Response is not a json format")

    assert token is not None, f"Токен для пользователя {login} не был получен"

    # 4 Активировать пользака

    url = f'http://5.63.153.31:5051/v1/account/{token}'

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    }

    response = requests.put(
        url,
        headers=headers
    )
    print(response.status_code)
    print(response.text)
    # # Пытаемся парсить JSON только если ответ не пустой
    # try:
    #     response_json = response.json()
    #     print("JSON Response:", response_json)
    #     pprint.pprint(response_json)
    # except requests.exceptions.JSONDecodeError:
    #     print("Ошибка: Сервер вернул невалидный JSON или пустой ответ.")
    assert response.status_code == 200, "Пользователь не был активирован"

    # # Авторизация

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/login', json=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"