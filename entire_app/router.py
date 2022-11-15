import io

# результат выполнения методов класса Router
class RouterResult:
    def __init__(self, body, type, sub_type=None, err=None):
        # контент
        self.body = body
        # тип контента
        self.type = type
        self.stype = sub_type

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