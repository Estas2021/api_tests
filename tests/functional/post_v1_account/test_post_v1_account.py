from json import (
    loads,
    JSONDecodeError,
)

import structlog


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            # sort_keys=True
        )
    ]
)

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from dm_api_mailhog.apis.mailhog_api import MailhogApi


def test_post_v1_account():
    # 1 регистрация пользака

    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')

    login = 'efremov_test23'
    password = '123456789'
    email = f'{login}@mail.ru'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = account_api.post_v1_account(json_data=json_data)

    assert response.status_code == 201, f"Пользак не был создан {response.json()}"

    # 2 Получение писем из почтового ящика

    response = mailhog_api.get_api_v2_messages()

    assert response.status_code == 200, "Письма не были получены"

    # 3 Получить активационный токен
    token = get_activation_token_by_login(login, response)

    assert token is not None, f"Токен для пользователя {login} не был получен"

    # 4 Активировать пользака

    response = account_api.put_v1_account_token(token=token)

    assert response.status_code == 200, "Пользователь не был активирован"

    # # Авторизация

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    assert response.status_code == 200, "Пользователь не смог авторизоваться"


def get_activation_token_by_login(
        login,
        response
):
    token = None
    try:
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']

            if user_login == login:
                # print('\n')
                # print(user_login)
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                # print(token)
    except JSONDecodeError:
        # print("Response is not a json format")
        return token
