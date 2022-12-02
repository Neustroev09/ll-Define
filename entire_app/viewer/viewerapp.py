
import os
import json

class ViewerApp:

    def __init__(self):
        self.page_avg_char_lengh = 1000
        self.clear_temp_books()
        
    def create_book(self, token, content):
        sents = self.split_into_sentenses(content)
        sents_obj = {i: v for i, v in enumerate(sents)}
        pages = self.split_into_pages(sents)
        pages_obj = {i: v for i, v in enumerate(pages)}
        self.save_book(token, {'sentences': sents_obj, 'pages': pages_obj})
        
    def save_book(self, token, book_content):
        with open('viewer\\temp_books\\' + token, 'w+', encoding='utf-8') as new_temp_f:
            json.dump(book_content, new_temp_f, ensure_ascii=False)
        
    def read_book(self, token):
        if os.path.isfile('viewer\\temp_books\\' + token):
            with open('viewer\\temp_books\\' + token, 'r', encoding='utf-8') as temp_store_list_f:  
                return json.load(temp_store_list_f)
        else:
            return None
        
    def split_into_sentenses(self, content):
        return content.split('.')
        
    def split_into_pages(self, sents):
        
        text_sentenses = sents
        
        flat_pages = ['']
        page_sents = [[]]
        current_page_id = 0
        
        for sent_n, sent in enumerate(text_sentenses):
            curr_sent_len = len(sent.strip())
            curr_page_len = len(flat_pages[current_page_id])
            if self.page_avg_char_lengh - (curr_page_len + curr_sent_len) >= 0:                
                curr_flat_page = flat_pages[current_page_id]  
                flat_pages[current_page_id] = curr_flat_page + sent.strip()
                page_sents[current_page_id].append(sent_n)
            else:    
                if abs(self.page_avg_char_lengh - curr_page_len) < abs(self.page_avg_char_lengh - (curr_page_len + curr_sent_len)):
                    flat_pages.append(sent.strip())
                    page_sents.append([sent_n])
                else:
                    curr_flat_page = flat_pages[current_page_id]  
                    flat_pages[current_page_id] = curr_flat_page + sent.strip()
                    page_sents[current_page_id].append(sent_n)
                    flat_pages.append('')
                    page_sents.append([])
                current_page_id += 1
        
        return page_sents
        
    def load_page(self, token, page_num): 
        book = self.read_book(token)
        if book:
            if str(page_num) not in book['pages']:
                return {}
            else:
                page = book['pages'][str(page_num)]
                result_page = {}
                for b_p in page:
                    result_page[b_p] = book['sentences'][str(b_p)]
                return result_page
        else:
            return {}
        
    def book_len(self, token):
        book = self.read_book(token)
        if book:
            return len(book['pages'])
        else:
            return None
            
    def clear_temp_books(self):
        dir = 'viewer\\temp_books\\'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))