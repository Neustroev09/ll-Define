# python3

import socket
import sys
import io
from email.parser import Parser
from urllib.parse import parse_qs, urlparse

import datetime
import hashlib
import json

#apps
from deflvl.deflvl import DefineLevelApp

# максимальная длина одного HTTP заголовка
MAX_LINE = 64*1024
# максимальное количество HTTP заголовков
MAX_HEADERS = 100

source_translator = {
    '/'             : ('html', 'pages\\main.html'),
    '/download'     : ('html', 'pages\\downloadTheBook.html'),
    '/test'         : ('html', 'pages\\passTheTest.html'),
    '/selection'    : ('html', 'pages\\selectionOfBooks.html'),
    '/act'          : ('html', 'pages\\readAndLevel.html'),
    '/result'          : ('html', 'pages\\testResults.html'),
    '/r/s1.css'     : ('css', 'res\\styles\\headerStyle.css'),
    '/r/s2.css'     : ('css', 'res\\styles\\bodyStyle.css'),
    '/r/s3.css'     : ('css', 'res\\styles\\testPageStyle.css'),
    '/r/p1.png'     : ('img', 'res\\images\\logo.png'),
    '/r/p2.png'     : ('img', 'res\\images\\dash.png'),
    '/r/p3.png'     : ('img', 'res\\images\\laptopAndPhone.png'),
    '/r/p4.png'     : ('img', 'res\\images\\bookLoading.png'),
    '/r/p5.png'     : ('img', 'res\\images\\grammarAnalysis.png'),
    '/r/p6.png'     : ('img', 'res\\images\\selectionLiterature.png'),
    '/r/p7.png'     : ('img', 'res\\images\\translationWords.png'),
    '/r/p8.png'     : ('img', 'res\\images\\testLevel.png'),
    '/r/p9.png'     : ('img', 'res\\images\\levelAnalysis.png'),
    '/r/p10.png'     : ('img', 'res\\images\\14678236.png'),
    '/r/p11.png'     : ('img', 'res\\images\\24532765.png'),
    '/r/p12.png'     : ('img', 'res\\images\\36478234.png'),
    '/r/p13.png'     : ('img', 'res\\images\\42398478.png'),
    '/r/f1.ttf'     : ('fnt', 'res\\fonts\\Montserrat-Bold.ttf'),
    '/r/f2.ttf'     : ('fnt', 'res\\fonts\\Montserrat-Medium.ttf'),
    '/r/f3.ttf'     : ('fnt', 'res\\fonts\\Montserrat-Light.ttf'),
    '/r/f4.ttf'     : ('fnt', 'res\\fonts\\Montserrat-Regular.ttf'),
}

def md5(some_str):
    return str(hashlib.md5(some_str.encode()).hexdigest())

# класс HTTP сервера
class MyHTTPServer:

    # конструктор класса
    def __init__(self, host, port, app = None):
        # хост или IP сервера
        self._host = host
        # Порт сервера (по умолчанию для HTTP серверов это 80)
        self._port = port
        # Добавляем в класс объект Router, для того, чтобы можно было пользоваться методами этого класса
        self._router = Router()
        
        self.app = app

    # главный метод сервера (функция запуска)
    def serve_forever(self):
        # сокет сервера
        serv_sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            proto=0)

        try:
            # пытаемся привязать сервер к хосту и потру
            serv_sock.bind((self._host, self._port))
            # ждем входящие запросы клиентов
            serv_sock.listen()
            # каждый момент времени accept() возвращает последний клиентский запрос 
            while True:
                # получаем сокет клиента (соединение с ним), из которого можно прочитать сам запрос
                conn, addres = serv_sock.accept()
                #try:
                # обрабатываем запрос клиента
                self.serve_client(conn, md5(addres[0]))
                #except Exception as e:
                #    print('Client serving failed', e)
        finally:
            # если что-то не так с кодом выше, то закрываем сокет и завершаем работу сервера
            serv_sock.close()

    # функция, обрабатывающая клиентский запрос
    def serve_client(self, conn, cl_ip_hashed):
        
        # пытаемся его обработать 
        try:
            # сначала достаем из него информацию
            req = self.parse_request(conn, cl_ip_hashed)
            # по заголовкам запроса составляем ответ (заголовки ответа + тело ответа)
            resp = self.route(req)
            # ну и наконец отправляем ответ
            self.send_response(conn, resp)
        except ConnectionResetError:
            # если возникает какая-то ошибка соединения, то зануляемм conn (его уже бесполезно закрывать в строке 75)
            conn = None
        except ServerError as e:
            # если возникает какая-то ошибка ServerError, то она попадает в send_error
            self.send_error(conn, e)

        # если с соединением все ок, то закрываем его
        if conn:
            conn.close()
    
    # функця, разбирающая запрос
    def parse_request(self, conn, cl_ip_hashed):
        # будем работать с запросом, как с файлом
        rfile = conn.makefile('rb')
        # парсим строку запроса, получаем метод, url страницы и версию протокола
        method, target, ver = self.parse_request_line(rfile)
        # затем парсим заголовки запроса
        headers = self.parse_headers(rfile)
        
        # если в запросе есть Content-Length (длина тела), то выгружаем тело запроса (POST запрос)
        # ОПАСНАЯ ХЕРНЯ, ЛУЧШЕ ТАК НЕ ДЕЛАТЬ
        body = None
        content_length = headers.get('Content-Length')
        if content_length:
            body = self.parse_body(rfile, headers.get('Content-Length'))
            
        # проверка на присутсвие хоста в заголовках (необязательная)
        host = headers.get('Host')
        if not host:
            raise ServerError(400, 'parse_request: host header is missing')
        
        rfile.close()
        
        # проверка самого хоста (тут она точно пока что не нужна т.к. запускаем сервер только на локальных машинах)
        #print(host, self._server_name, self._server_name, self._port)
        #if host not in (self._server_name, f'{self._server_name}:{self._port}'):
        #    raise HTTPError(404, 'Not found 63')
        
        # возвращаем объект запроса
        return Request(cl_ip_hashed, method, target, ver, headers, rfile, body)

    # функция, обрабатывающая строку запроса
    def parse_request_line(self, rfile):
        # считываем эту строку
        raw = rfile.readline(MAX_LINE + 1)
        # проверяем ее длину
        if len(raw) > MAX_LINE:
            raise ServerError(400, 'parse_request_line: request line is too long')
        
        # переводим строку кодировки iso-8859-1 в питоновский строковый объект 
        req_line = str(raw, 'iso-8859-1')
        # разбиваем строку на слова (с пробелом в качестве разделителя)
        words = req_line.split()
        # если количество слов != 3, то это ошибка
        if len(words) != 3:
            raise ServerError(400, 'parse_request_line: malformed request line')

        # всего слов 3 - это HTTP метод, URL страницы и версия протокола
        method, target, ver = words
        # проверяем версию протокола 
        if ver != 'HTTP/1.1':
            raise ServerError(505, 'parse_request_line: HTTP version not supported')
        
        # возращаем эти слова
        return method, target, ver

    # функция, достающая заголовки из запроса
    def parse_headers(self, rfile):
        # список заголовков
        headers = []
        # парсим заголовки построчно в бесконечном цикле
        while True:
            # считываем очередную строку
            line = rfile.readline(MAX_LINE + 1)
            # проверяем ее длину
            if len(line) > MAX_LINE:
                raise ServerError(494, 'parse_headers: request header too large')
            
            # если текущая строка является завершающим символом (это переносы строк или так называемый нулевой символ), то выходим из бесконечного цикла
            if line in (b'\r\n', b'\n', b''):
                break
    
            # добавляем в headers текущую строчку
            headers.append(line)
            # проверяем количество заголовков
            if len(headers) > MAX_HEADERS:
                raise ServerError(494, 'parse_headers: too many headers')
        
        # объедиеняем все заголовки обрабатно в строку (по сути получается те же заголовки, что и в начале, но без завершающего символа)
        sheaders = b''.join(headers).decode('iso-8859-1')
        # конверитируем заголовки в питоновский словарь с помощью магической функции
        # пример "Host: iidefine.com\nUser-Agent: Mozila/5.0" -> {"Host": "iidefine.com", "User-Agent": "Mozila/5.0"}
        return Parser().parsestr(sheaders)

    def parse_body(self, rfile, clen = 0):
    
        body = None
        try:
            body = rfile.read(int(clen))
        except:
            raise ServerError(400, 'parse_body: some problems with body reading')
        
        return body

    def parse_file_info(self, raw_body):
    
        body = raw_body
    
        try:
            body = str(body, 'iso-8859-1')
            body = body[body.find('\r\n')+2:]
            body = body[:body.find('\r\n------')]
        except:
            raise ServerError(400, 'parse_file_info: wrong body format 1')
        
        body_obj = {}
        try:
            body = Parser().parsestr(body)
            for key, val in body.items():
                body_obj[key] = val
            body_obj['Body'] = body.get_payload()
        except:
            raise ServerError(400, 'parse_file_info: wrong body format 2')
        
        if 'Content-Disposition' not in body_obj:
            raise ServerError(400, 'parse_file_info: wrong body format 3')
         
        # НАДО НЕ ЗАБЫТЬ ЗДЕСЬ ПРОВЕРИТЬ НАЗВАНИЕ ВНУТРЕННЕГО ПОЛЯ
        try:
            cd_fields = body_obj['Content-Disposition'].split(';')
            new_cd_obj = {}
            for cdf in cd_fields:
                cl_cdf = cdf.strip()
                field_name_val = cl_cdf.split('=')
                if len(field_name_val) == 2:
                    new_cd_obj[field_name_val[0]] = field_name_val[1][1:-1]
        except:
            raise ServerError(400, 'parse_file_info: wrong body format 3')
        
        body_obj['Content-Disposition'] = new_cd_obj
        
        return body_obj

    # функция обрабатывыающая запрос пользователя (этот процесс иногда называют routing'ом)
    def route(self, req):
        # в router_result будет хранится возвращаемый контент и его тип(например, HTML страничка и ее тип 'html')
        router_result = None
        # если путь (все то, что находится в URL после https://iidefine.com) пуст или равен '/' и метод GET (классисеский метод, который используют браузеры для получаения страниц сайтов)
        
        if req.method == 'GET':
            if req.path in source_translator:
                site_source = source_translator[req.path]
                if site_source[0] == 'html':
                    router_result = self._router.html_page(site_source[1])
                elif site_source[0] == 'css':
                    router_result = self._router.styles_file(site_source[1])
                elif site_source[0] == 'img':
                    router_result = self._router.image_file(site_source[1])       
                elif site_source[0] == 'fnt':
                    router_result = self._router.font_file(site_source[1])  
        
        if req.method == 'POST':
            if req.path == '/loadbook':
                ref = req.headers.get('Referer')
                if ref and ref.split('/')[-1] == 'download':
                    req.body = self.parse_file_info(req.body)
                    book_file_name = req.body['Content-Disposition']['filename']
                    book_type = req.body['Content-Type']
                    book_text = req.body['Body']
                    
                    token = self.app.load_book(req.hashed_ip, book_file_name, book_type, book_text)
                    
                    router_result = self._router.redirect('/act?t='+token)
            
        router_result = self.dynamic_content(req, router_result)
            
        # если router_result не пустой, то
        if router_result:
            # добавляем к этому контенту заголовки и возвращаем обратно
            return self.constuct_response(router_result)
        else:
            # иначе 404-ая ошибка
            raise ServerError(404, f'route: page "{req.path}" not found')

    def dynamic_content(self, req, router_result):
    
        new_router_result = router_result
    
        if req.method == 'GET':
            if req.path == '/act':
                url_params = req.url.query.split('&')
                if len(url_params) == 1:
                    param_name, param_value = url_params[0].split('=')
                    if param_name == 't':
                        book_info = self.app.get_book_info_with_token(param_value)
                        if book_info:
                            datetime = book_info['time'].split()
                            new_router_result.body = new_router_result.body\
                                .replace('#BOOK_NAME#', book_info['name'])\
                                .replace('#BOOK_DATE#', datetime[0])\
                                .replace('#BOOK_TIME#', datetime[1][:8])
                        else:
                            raise ServerError(404, f'dynamic_content: token {param_value} not found')
                    else:
                        raise ServerError(404, f'dynamic_content: problems with name of t parameter')
                else:
                    raise ServerError(404, f'dynamic_content: problems with number of url params')
        
            if req.path == '/deflvl':
                url_params = req.url.query.split('&')
                if len(url_params) == 1:
                    param_name, param_value = url_params[0].split('=')
                    if param_name == 't':
                        book_info = self.app.get_book_info_with_token(param_value)
                        if book_info:
                            with open('temp_store\\temp_books\\' + book_info['token'], 'r', encoding='utf-8') as temp_book:  
                                book_text = temp_book.read()
                                new_router_result = RouterResult(self.app.define.define_level(book_text), 'html')
                        else:
                            raise ServerError(404, f'dynamic_content: token {param_value} not found (deflvl)')
                    else:
                        raise ServerError(404, f'dynamic_content: problems with name of t parameter (deflvl)')
                else:
                    raise ServerError(404, f'dynamic_content: problems with number of url params (deflvl)')
        
        print(new_router_result.body)
        
        return new_router_result

    # функция, добавляющая к возвращаемому контенту заголовки (заголовки ответа)
    def constuct_response(self, router_result):
        # если тип контента == 'html'
        if router_result.type == 'html':
            # переводим питоновскую строку в кодировку UTF-8
            body = router_result.body.encode('utf-8')
            # значение одного из заголовков, которое отвечает за тип контента
            contentType = 'text/html; charset=utf-8'
            # заголовки ответа
            headers = [('Content-Type', contentType),
                       ('Content-Length', len(body))]
            # возвращаем объект, который помимо заголовков и контента хранит в себе статус и сообщение (это составляющие строки ответа)
            return Response(200, 'OK', headers, body)
            
        elif router_result.type == 'css':
            # переводим питоновскую строку в кодировку UTF-8
            body = router_result.body.encode('utf-8')
            # значение одного из заголовков, которое отвечает за тип контента
            contentType = 'text/css; charset=utf-8'
            # заголовки ответа
            headers = [('Content-Type', contentType),
                       ('Content-Length', len(body))]
            # возвращаем объект, который помимо заголовков и контента хранит в себе статус и сообщение (это составляющие строки ответа)
            return Response(200, 'OK', headers, body)
            
        elif router_result.type == 'img':
            # переводим питоновскую строку в кодировку UTF-8
            body = router_result.body
            # значение одного из заголовков, которое отвечает за тип контента
            contentType = f'image/{router_result.stype}'
            # заголовки ответа
            headers = [('Content-Type', contentType),
                       ('Content-Length', len(body))]
            # возвращаем объект, который помимо заголовков и контента хранит в себе статус и сообщение (это составляющие строки ответа)
            return Response(200, 'OK', headers, body)
            
        elif router_result.type == 'font':
            # переводим питоновскую строку в кодировку UTF-8
            body = router_result.body
            # значение одного из заголовков, которое отвечает за тип контента
            font_mime_translate = {
                'ttf' : 'application/x-font-ttf',
                'otf' : 'application/x-font-opentype'
            }
            contentType = font_mime_translate[router_result.stype]
            # заголовки ответа
            headers = [('Content-Type', contentType),
                       ('Content-Length', len(body))]
            # возвращаем объект, который помимо заголовков и контента хранит в себе статус и сообщение (это составляющие строки ответа)
            return Response(200, 'OK', headers, body)
            
        elif router_result.type == 'redirect':
            headers = [('Location', router_result.stype)]
            return Response(303, 'See Other', headers, '')
            
        # если контент имеет какой-то странный тип (или не имеет его вовсе) инициируем ошибку
        raise ServerError(500, 'constuct_response: internal error')

    # функция, отправляющая ответ клиенту
    def send_response(self, conn, resp):
        # будем работать с ответом как с файлом (т.е. этот файл как-бы будет отправлен клиенту)
        wfile = conn.makefile('wb')
        # формируем строку ответа
        status_line = f'HTTP/1.1 {resp.status} {resp.reason}\r\n'
        # записываем ее в файл
        wfile.write(status_line.encode('iso-8859-1'))

        # если есть заголовки ответа, то записываем их тоже
        if resp.headers:
            for (key, value) in resp.headers:
                header_line = f'{key}: {value}\r\n'
                wfile.write(header_line.encode('iso-8859-1'))
        # записываем завершающий символ (в ответе он играет роль разделителя заголовков и контента)
        wfile.write(b'\r\n')
        # записываем сам контент
        if resp.body:
            wfile.write(resp.body)
        # очищаем буфер и закрываем файл (т.е. отправляем ответ)
        wfile.flush()
        wfile.close()

    # функция, отправляющая страницы с ошибками (404 например)
    def send_error(self, conn, err):
        
        # если есть какое-то внутренее сообщение, то выводим его (это второй параметр конструктора ServerError)
        if err.body:
            print(err.body)
            
        # словарь с расшифровками HTTP ошибок
        err_reasons = {
            400: 'Bad request',
            404: 'Not found',
            494: 'Request header too large',
            500: 'Internal Server Error',
            505: 'HTTP Version Not Supported',
        }
        
        # пытаемся определиться со статусом и описанием ошибки (из err_reasons)
        try:
            status = err.status
            reason = err_reasons[err.status]
        except:
            status = 500
            reason = err_reasons[500]
        
        # генерируем контент страницы с ошибкой
        err_page = self._router.error_page(status, reason)
        # меняем кодировку
        body = err_page.body.encode('utf-8')
        # добавляем к контенту заголовки ответа
        resp = Response(status, reason,
                                     [('Content-Length', len(body))],
                                     body)
        # отправляем ответ пользователю
        self.send_response(conn, resp)
        

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

# класс, объекты которого создаются при возникновении каких-либо ошибок (обрабатываются функцией send_error, см. строку 70)
class ServerError(Exception): 
    def __init__(self, status, body=None):
        # выполнение страндартной ошибки Python
        super()
        # добавляем к объекту стандартной ошибки статус и пояснение (где появилась ошибка и что она из себя представляет)
        self.status = status
        self.body = body

# класс, методы которого возращают контент сайта (например, html странички)
class Router:
    def __init__(self):
        pass
    
    def html_page(self, page_loc):
        file = io.open(page_loc, mode='r', encoding='utf-8')
        resp_body = file.read()
        file.close()
        return RouterResult(resp_body, 'html')
    
    def styles_file(self, file_loc):
        file = io.open(file_loc, mode='r', encoding='utf-8')
        resp_body = file.read()
        file.close()
        return RouterResult(resp_body, 'css')
        
    def image_file(self, file_loc):
        file = io.open(file_loc, mode='rb')
        resp_body = file.read()
        file.close()
        return RouterResult(resp_body, 'img', file_loc.split('.')[-1])
        
    def font_file(self, file_loc):
        file = io.open(file_loc, mode='rb')
        resp_body = file.read()
        file.close()
        return RouterResult(resp_body, 'font', file_loc.split('.')[-1])
    
    # скелет для всех страничек с ошибками
    def error_page(self, status, body):
        body = '<style>@font-face{font-family:Montserrat-Bold;src:url(../r/f1.ttf);}</style>' \
            '<body style="font-family:Montserrat-Bold;color: #333;">' \
            '<div style="width: 100%; text-align:center; margin-top:100px;">' \
            f'<h1 style="font-size:6em;color:#b0dddc"><i>#lldefine{status}</i></h1><h2 style="font-size:3em">{body}</h2>' \
            '</div></body>'
        return RouterResult(body, 'html')
        
    def redirect(self, new_url):
        return RouterResult(None, 'redirect', new_url)

# результат выполнения методов класса Router
class RouterResult:
    def __init__(self, body, type, sub_type=None, err=None):
        # контент
        self.body = body
        # тип контента
        self.type = type
        self.stype = sub_type


class LLdefineApp:
    def __init__(self, def_app):
        self.define = def_app
        self.clear_temp_list()

    def load_book(self, client_id, book_name, book_type, book_text):
        
        token = self.constuct_token(client_id, book_name)
        
        if not self.get_book_info_with_token(token):
            self.save_into_temp_list(client_id, book_name, book_type, book_text, token)
            self.save_temp_book(token, book_text)
            print('LLdefineApp: book with new token has been saved')
        else:
            print('LLdefineApp: book with such token already exists')
            
        return token
        
    def save_temp_book(self, token, book_text):
    
        with open('temp_store\\temp_books\\' + token, 'w+', encoding='utf-8') as new_temp_f:
            new_temp_f.write(book_text)
        
    def save_into_temp_list(self, client_id, book_name, book_type, book_text, token):

        with open('temp_store\\temp_store_list.json', 'r', encoding='utf-8') as temp_store_list_f:  
            temp_store_list = json.load(temp_store_list_f)
            if not temp_store_list:
                temp_store_list = []
            temp_store_list.append({'client': client_id, 'name': book_name, 'type': book_type, 'time': datetime.datetime.now(), 'token': token})
            
        with open('temp_store\\temp_store_list.json', 'w', encoding='utf-8') as temp_store_list_f:  
            json.dump(temp_store_list, temp_store_list_f, ensure_ascii=False, default=str)

    def clear_temp_list(self):
        with open('temp_store\\temp_store_list.json', 'w', encoding='utf-8') as temp_store_list_f:  
            json.dump([], temp_store_list_f, ensure_ascii=False)

    def constuct_token(self, client_id, book_name):
        return md5(client_id + book_name)
        
    def get_book_info_with_token(self, token):
    
        with open('temp_store\\temp_store_list.json', 'r', encoding='utf-8') as temp_store_list_f:  
            temp_store_list = json.load(temp_store_list_f)
            if temp_store_list:
                ex_tokens = [x for x in temp_store_list if x['token'] == token]
                if len(ex_tokens) == 0:
                    return None
                elif len(ex_tokens) == 1:
                    return ex_tokens[0]
                else:
                    raise ServerError(500, f'get_book_info_with_token: several records with the same token in temp_store_list')
        
        return None
    

# если данный файл является основным (главный цикл питоновской программы)
if __name__ == '__main__':

    # записываем основные параметры сервера
    host = '127.0.0.1'
    port = 80

    def_lvl_app = DefineLevelApp()
    def_lvl_app.init_app()

    our_app_instance = LLdefineApp(def_lvl_app)

    # создаем его объект
    serv = MyHTTPServer(host, port, our_app_instance)
    
    # и наконец запускаем
    #try:
    serv.serve_forever()
    #except KeyboardInterrupt:
    #    exit()