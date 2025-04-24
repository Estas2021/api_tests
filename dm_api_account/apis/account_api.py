import requests
from restclient.client import RestClient

# class AccountApi:                  # было до RestClient
#     def __init__(
#             self,
#             host,
#             headers=None
#     ):
#         self.host = host
#         self.headers = headers
#
#     def post_v1_account(
#             self,
#             json_data
#     ):
#         """
#         Register new user
#         :param json_data:
#         :return:
#         """
#         response = requests.post(
#             url=f'{self.host}/v1/account',
#             json=json_data
#         )
#         return response
#
#     def put_v1_account_token(
#             self,
#             token
#     ):
#         """
#         Activate registered user
#         :param token:
#         :return:
#         """
#         headers = {
#             'accept': 'text/plain',
#         }
#
#         response = requests.put(
#             url=f'http://5.63.153.31:5051/v1/account/{token}',
#             headers=headers
#         )
#         return response

class AccountApi(RestClient):   # исп-ем механизм наследования для исп-я методов и функций из него

    def post_v1_account(
            self,
            json_data
    ):
        """
        Register new user
        :param json_data:
        :return:
        """
        response = self.post(           # не исп-ем библу requests: исп-ем теперь RestClient
            path='/v1/account',
            json=json_data
        )
        return response

    def put_v1_account_token(
            self,
            token
    ):
        """
        Activate registered user
        :param token:
        :return:
        """
        headers = {
            'accept': 'text/plain',
        }

        response = self.put(
            path=f'/v1/account/{token}',
            headers=headers
        )
        return response
