from json import JSONDecodeError

from requests import session  # специальный объект через которые будут вып-ся все запросы
import structlog
import uuid
import curlify

from restclient.configuration import Configuration


class RestClient:
    def __init__(
            self,
            configuration: Configuration
    ):
        self.host = configuration.host
        self.headers = configuration.headers
        self.disable_log = configuration.disable_log
        self.session = session()
        self.log = structlog.get_logger(__name__).bind(service='api')  # иниц-я логгера для его исп-я
        # в кач-ве названия логгера берется название класса RestClient через параметр __name__

    # внутри методов вызываем _send_request после логгирования запросов с ответами
    def post(
            self,
            path,
            **kwargs
    ):
        return self._send_request(method='POST', path=path, **kwargs)

    def get(
            self,
            path,
            **kwargs
    ):
        return self._send_request(method='GET', path=path, **kwargs)

    def put(
            self,
            path,
            **kwargs
    ):
        return self._send_request(method='PUT', path=path, **kwargs)

    def delete(
            self,
            path,
            **kwargs
    ):
        return self._send_request(method='DELETE', path=path, **kwargs)

    def _send_request(
            self,
            method,
            path,
            **kwargs
    ):  # метод для логгирования запросов, для кот нужна библа structlog
        log = self.log.bind(event_id=str(uuid.uuid4()))  # получение id для каждого запроса логгера
        full_url = self.host + path

        if self.disable_log:
            rest_response = self.session.request(method=method, url=full_url, **kwargs)
            return  rest_response

        # логгируем наш запрос
        log.msg(
            event='Request',
            method=method,
            full_url=full_url,
            params=kwargs.get('params'),
            headers=kwargs.get('headers'),
            json=kwargs.get('json'),
            data=kwargs.get('data'),
        )

        # из под сессии выполняем запрос
        rest_response = self.session.request(method=method, url=full_url, **kwargs)
        curl = curlify.to_curl(rest_response.request)
        print(curl)

        # логгируем ответ
        log.msg(
            event='Response',
            status_code=rest_response.status_code,
            headers=rest_response.headers,
            # json=rest_response.json(), было до _get_json()
            json=self._get_json(rest_response),
        )
        return rest_response

    @staticmethod       # не исп-ет функции и параметры внутри класса выше
    def _get_json(
            rest_response
    ):
        try:
            return rest_response.json()
        except JSONDecodeError:
            return {}
