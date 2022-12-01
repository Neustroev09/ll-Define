
from googletrans import Translator

class TranslateApp:

    def __init__(self):
        self.translator = Translator()

    def preprocess(self, text):
        return text.replace('’', '\'')

    def en2ru(self, text):
        tt = self.preprocess(text)
        return self.translator.translate(tt, src="en", dest="ru").text