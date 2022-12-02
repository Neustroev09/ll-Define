# python3

#apps
from lldefineapp import LLdefineApp
from deflvl.deflvl import DefineLevelApp
from translate.translate import TranslateApp
from grammar.grammar import GrammarApp
from viewer.viewerapp import ViewerApp
from http_server import HTTPServer

# если данный файл является основным (главный цикл питоновской программы)
if __name__ == '__main__':

    # записываем основные параметры сервера
    host = '127.0.0.1'
    port = 8080

    def_lvl_app = DefineLevelApp()
    viewer_app = ViewerApp()
    translate_app = TranslateApp()
    grammar_app = GrammarApp()
    
    grammar_app.init_app()
    def_lvl_app.init_app()

    our_app_instance = LLdefineApp(def_lvl_app, translate_app, grammar_app, viewer_app)

    # создаем его объект
    serv = HTTPServer(host, port, our_app_instance)
    
    # и наконец запускаем
    #try:
    serv.serve_forever()
    #except KeyboardInterrupt:
    #    exit()