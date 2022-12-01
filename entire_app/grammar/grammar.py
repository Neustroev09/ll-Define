
import nltk
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import state_union, brown
from nltk.tokenize import sent_tokenize
from nltk.tokenize import WhitespaceTokenizer
from nltk.tokenize import RegexpTokenizer

import re

class GrammarApp:

    def __init__(self):
        pass
        
    def init_app(self):
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('tagsets')
        nltk.download('brown')
        
    def preprocess(self, text):
        text = re.sub(r'[^\w\s\,\;]','', text)
        text = text.replace('cannot', "can not")  
        text2 = nltk.word_tokenize(text)
        tagged_ = nltk.pos_tag(text2)
        return tagged_
        
    def def_tense(self, text):
        try:
            tagged_ = self.preprocess(text)

            verb_tags = ['MD','MDF','VB','VBP','VBZ','VBD','VBG','VBN']  
            verb_phrase = []

            for item in tagged_:
                if item[1] in verb_tags:
                    verb_phrase.append(item)

            grammar = r'''
                Present Cotinuous: {<VBP><VBG>}
                Past Continuous: {<VBD><VBG>}

                Future Continuous: {<MD><VB><VBG>}

                Future Perfect Continuous: {<MD><VB><VBN><VBG>}
                Future Perfect Continuous_won: {<VBP><VBN><VBG>}
                Future Perfect Continuous: {<MD><VB|VBP><VBN><VBG>}

                Future Perfect: {<MD><VB|VBP><VBN>}
                Future Perfect: {<VBD><PRP><VBP><VBN>}
                Future Perfect: {<MD><VB|VBP><VBN>}

                Present Perfect Continuous: {<VBP|VBZ><VBN><VBG>}
      
                Past Perfect Continuous: {<VBD|VBN><VBG>}

                Present Perfect: {<VBP|VBZ><VBN>}
                Present Perfect: {<VBP|VBZ><VBD|VBN>}

                Past Perfect Continuous: {<VBD><VBN><VBG>}
                Past Perfect: {<VBD|VBP><VBN|VB|VBP>}
           
                Future Simple: {<MD><VB>}
                Future Simple: {<MD><VB|VBP|VBZ>}
                Present Simple: {<VBP|VBZ|VB>}  
                Past Simple: {<VBD>}      
            '''
            
            cp = nltk.RegexpParser(grammar)
            result = cp.parse(verb_phrase)
                          
            tenses_set = []
            result2 = []
            
            for node in result:
                if type(node) is nltk.tree.Tree:
                    tenses_set.append(node.label())
                    result2.append(node.pos())
            return result2
            
        except:
            return []

    def tok_pos(self, predl):  
      
        text = re.sub(r'[^\w\s\,\;]','', predl)
        tokens_positions = list(WhitespaceTokenizer().span_tokenize(text))  
        tokens = WhitespaceTokenizer().tokenize(text)  

        tokens = nltk.pos_tag(tokens) 

        words = []
        for i in range(len(tokens)):
            text, tag = tokens[i]  
            start, end = tokens_positions[i]  
            if tag in ['MD','MDF', 'VB','VBP','VBZ','VBD','VBG','VBN']:
                words.append((start, end, tag, text))

        return words
        
    def tenses(self, text):
        
        f1_r = self.def_tense(text)
        f2_r = self.tok_pos(text)
        
        real_res = []
        
        for f1_r_e in f1_r:
            for f2_r_e in f2_r:
                if f1_r_e[0][0][0] in f2_r_e and f1_r_e[0][0][1] in f2_r_e:
                    real_res.append({'index': [*f2_r_e[:2]], 'tense': f1_r_e[0][1]})
        
        return real_res
        