
import socket
import json
from email.parser import Parser
from urllib.parse import parse_qs, urlparse, unquote

from router import Router, RouterResult
from toolfuns import md5
from errors import ServerError
from server_packs import Response, Request

# максимальная длина одного HTTP заголовка
MAX_LINE = 64*1024
# максимальное количество HTTP заголовков
MAX_HEADERS = 100

# класс HTTP сервера
class HTTPServer:

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
        # декодим спец символы URL
        target = unquote(target)
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
            body = str(body, 'utf-8')
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

    def st(self, source_key):
        with open('source_translator.json', 'r', encoding='utf-8') as st: 
            st_obj = json.load(st)
            if source_key in st_obj:
                return tuple(st_obj[source_key])
            return None
            
    # функция обрабатывыающая запрос пользователя (этот процесс иногда называют routing'ом)
    def route(self, req):
        # в router_result будет хранится возвращаемый контент и его тип(например, HTML страничка и ее тип 'html')
        router_result = None
        # если путь (все то, что находится в URL после https://iidefine.com) пуст или равен '/' и метод GET (классисеский метод, который используют браузеры для получаения страниц сайтов)
        
        if req.method == 'GET':
            site_source = self.st(req.path)
            if site_source:
                if site_source[0] == 'html':
                    router_result = self._router.html_page(site_source[1])
                elif site_source[0] == 'css':
                    router_result = self._router.styles_file(site_source[1])
                elif site_source[0] == 'img':
                    router_result = self._router.image_file(site_source[1])       
                elif site_source[0] == 'fnt':
                    router_result = self._router.font_file(site_source[1])  
                elif site_source[0] == 'js':
                    router_result = self._router.js_file(site_source[1])
                elif site_source[0] == 'mp3':
                    router_result = self._router.mp3_file(site_source[1])

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
        
            elif req.path == '/deflvl':
                url_params = req.url.query.split('&')
                if len(url_params) == 1:
                    param_name, param_value = url_params[0].split('=')
                    if param_name == 't':
                        book_info = self.app.get_book_info_with_token(param_value)
                        if book_info:
                            book_text = self.app.read_temp_book(book_info['token'])
                            new_router_result = RouterResult(self.app.define.define_test(book_text), 'html')
                        else:
                            raise ServerError(404, f'dynamic_content: token {param_value} not found (deflvl)')
                    else:
                        raise ServerError(404, f'dynamic_content: problems with name of t parameter (deflvl)')
                else:
                    raise ServerError(404, f'dynamic_content: problems with number of url params (deflvl)')

            elif req.path == '/read':
                url_params = req.url.query.split('&')
                if len(url_params) == 1:
                    param_name, param_value = url_params[0].split('=')
                    if param_name == 't':
                        book_info = self.app.get_book_info_with_token(param_value)
                        if book_info:
                            book_len = self.app.viewer.book_len(book_info['token'])
                            if not book_len:
                                self.app.viewer.create_book(book_info['token'], self.app.read_temp_book(book_info['token']))
                                book_len = self.app.viewer.book_len(book_info['token'])
                            new_router_result.body = new_router_result.body\
                                .replace('#BOOK_LAST_PAGE_NUMBER#', str(book_len - 1))
                        else:
                            raise ServerError(404, f'dynamic_content: token {param_value} not found (read)')
                    else:
                        raise ServerError(404, f'dynamic_content: problems with name of t parameter (read)')
                else:
                    raise ServerError(404, f'dynamic_content: problems with number of url params (read)')
                    
            elif req.path == '/pc':
                url_params = req.url.query.split('&')
                if len(url_params) == 2:
                    param1_name, param1_value = url_params[0].split('=')
                    param2_name, param2_value = url_params[1].split('=')
                    if param1_name == 't' and param2_name == 'pn':
                        book_info = self.app.get_book_info_with_token(param1_value)
                        if book_info:
                            page_content = self.app.viewer.load_page(book_info['token'], int(param2_value))
                            new_router_result = RouterResult(json.dumps(page_content, default=lambda o: o.__dict__), 'html')
                        else:
                            raise ServerError(404, f'dynamic_content: token {param_value} not found (pc)')
                    else:
                        raise ServerError(404, f'dynamic_content: problems with name of parameters (pc)')
                else:
                    raise ServerError(404, f'dynamic_content: problems with number of url params (pc)')
                    
            elif req.path == '/e2r':
                url_params = req.url.query.split('&')
                if len(url_params) == 2:
                    param1_name, param1_value = url_params[0].split('=')
                    param2_name, param2_value = url_params[1].split('=')
                    if param1_name == 't' and param2_name == 'w':
                        book_info = self.app.get_book_info_with_token(param1_value)
                        if book_info:
                            page_content = self.app.translate.en2ru(param2_value)
                            new_router_result = RouterResult(page_content, 'html')
                        else:
                            raise ServerError(404, f'dynamic_content: token {param_value} not found (pc)')
                    else:
                        raise ServerError(404, f'dynamic_content: problems with name of parameters (pc)')
                else:
                    raise ServerError(404, f'dynamic_content: problems with number of url params (pc)')
            
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
            
        if router_result.type == 'js':
            # переводим питоновскую строку в кодировку UTF-8
            body = router_result.body.encode('utf-8')
            # значение одного из заголовков, которое отвечает за тип контента
            contentType = 'text/javascript; charset=utf-8'
            # заголовки ответа
            headers = [('Content-Type', contentType),
                       ('Content-Length', len(body))]
            # возвращаем объект, который помимо заголовков и контента хранит в себе статус и сообщение (это составляющие строки ответа)
            return Response(200, 'OK', headers, body)

        if router_result.type == 'mp3':
            # переводим питоновскую строку в кодировку UTF-8
            body = router_result.body
            # значение одного из заголовков, которое отвечает за тип контента
            contentType =  f'mp3/{router_result.stype}'
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