
from email.parser import Parser
from urllib.parse import parse_qs, urlparse

# класс, объекты которого хранят данные клиентских запросов 
class Request:
    def __init__(self, client_ip_hashed, method, target, version, headers, rfile, body = None):
        # захешированный ip пользователя
        self.hashed_ip = client_ip_hashed
        # метод запроса
        self.method = method
        # url запроса
        self.target = target
        # версия http протокола
        self.version = version
        # заголовки запроса
        self.headers = headers
        # файл, который используется для чтения запроса
        self.rfile = rfile
        
        self.body = body
        
        # url, разбитый на части
        self.url = urlparse(self.target)
        # часть url, идущая после хоста
        self.path = self.url.path

    # функция, возвращающая тело запроса (если оно есть)
    def body(self):
        size = self.headers.get('Content-Length')
        if not size:
            return None
        return self.rfile.read(size)

# класс, объекты которого хранят данные ответов
class Response:
    def __init__(self, status, reason, headers=None, body=None):
        # статус (часть строки ответа)
        self.status = status
        # расшифровка HTTP статуса ответа (часть строки ответа)
        self.reason = reason
        # заголовки ответа
        self.headers = headers
        # тело ответа (непосредственно контент страниц сайта)
        self.body = body