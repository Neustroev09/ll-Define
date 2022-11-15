# python3

#apps
from lldefineapp import LLdefineApp
from deflvl.deflvl import DefineLevelApp
from http_server import HTTPServer

# если данный файл является основным (главный цикл питоновской программы)
if __name__ == '__main__':

    # записываем основные параметры сервера
    host = '127.0.0.1'
    port = 80

    def_lvl_app = DefineLevelApp()
    #def_lvl_app.init_app()

    our_app_instance = LLdefineApp(def_lvl_app)

    # создаем его объект
    serv = HTTPServer(host, port, our_app_instance)
    
    # и наконец запускаем
    #try:
    serv.serve_forever()
    #except KeyboardInterrupt:
    #    exit()