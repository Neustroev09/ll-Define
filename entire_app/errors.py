

# класс, объекты которого создаются при возникновении каких-либо ошибок (обрабатываются функцией send_error, см. строку 70)
class ServerError(Exception): 
    def __init__(self, status, body=None):
        # выполнение страндартной ошибки Python
        super()
        # добавляем к объекту стандартной ошибки статус и пояснение (где появилась ошибка и что она из себя представляет)
        self.status = status
        self.body = body
