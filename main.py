import pprint
import requests

# request = requests.request('post',)
# url = 'http://5.63.153.31:5051/v1/account'
#
# headers = {
#     'accept': '*/*',
#     'Content-Type': 'application/json',
# }
#
# json_data = {
#     'login': 'efremov_test2',
#     'email': 'efremov_test2@mail.ru',
#     'password': '123456789',
# }
#
# response = requests.post('http://5.63.153.31:5051/v1/account', headers=headers, json=json_data)
# print(response.status_code)


url = 'http://5.63.153.31:5051/v1/account/0461927a-1657-494a-acdf-24045a987072'

headers = {
    'accept': '*/*',
}
response = requests.put(
    url,
    headers=headers
)

# Проверяем HTTP-статус ответа
print("Status Code:", response.status_code)

# Смотрим сырой ответ перед парсингом JSON
print("Raw Response:", response.text)

# Пытаемся парсить JSON только если ответ не пустой
try:
    response_json = response.json()
    print("JSON Response:", response_json)
    pprint.pprint(response_json)
    print(response_json['resource']['rating'].get('quantity', 'dick tam!'))
    # print(response_json.get('resource')('rating')('quantity'))
except requests.exceptions.JSONDecodeError:
    print("Ошибка: Сервер вернул невалидный JSON или пустой ответ.")
