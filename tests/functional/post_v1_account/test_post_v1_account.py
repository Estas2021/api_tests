import time
from json import (
    loads,
    JSONDecodeError,
)
import structlog

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as DmApiConfiguration
from restclient.configuration import Configuration as MailhogConfiguration

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            # sort_keys=True
        )
    ]
)

from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount

def test_post_v1_account():
# 1 регистрация пользака

    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog) # мегаФАСАД

    login = 'efremov_test41'
    password = '123456789'
    email = f'{login}@mail.ru'

    account_helper.register_new_user(login=login,password=password,email=email)

    account_helper.login_user(login=login, password=password)





