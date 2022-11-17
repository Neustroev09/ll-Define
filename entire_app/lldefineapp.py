
import datetime
import json

from toolfuns import md5
from errors import ServerError

class LLdefineApp:
    def __init__(self, def_app, view_app):
        self.define = def_app
        self.viewer = view_app
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
        
    def read_temp_book(self, token):
        with open('temp_store\\temp_books\\' + token, 'r', encoding='utf-8') as temp_book:  
            book_text = temp_book.read()
            return book_text