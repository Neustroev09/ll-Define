
import nltk
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import state_union, brown
from nltk.tokenize import sent_tokenize
from nltk.tokenize import WhitespaceTokenizer
from nltk.tokenize import RegexpTokenizer

import re

class GrammarApp:

    def __init__(self, init=True):
        self.init = init
        if init:
            self.init_app()
        
    def init_app(self):
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('tagsets')
        nltk.download('brown')
        
    def preprocess(self, text):
        #text = re.sub(r'[^\w\s\,\;]','', text)
        #text = text.replace('cannot', "can not")  
        text2 = nltk.word_tokenize(text)
        tagged_ = nltk.pos_tag(text2)
        return tagged_
        
    def def_tense(self, text):
        try:
            tagged_ = self.preprocess(text)

            verb_tags = ['MD','MDF','VB','VBP','VBZ','VBD','VBG','VBN','TO']  
            verb_phrase = []

            for item in tagged_:
                if item[1] in verb_tags:
                    verb_phrase.append(item)

            grammar = r'''
                Present Cotinuous: {<VBP><VBG>+}
                Past Continuous: {<VBD><VBG>+}

                Future Continuous: {<MD><VB><VBG>+}

                Future Perfect Continuous: {<MD><VB><VBN><VBG>+}
                Future Perfect Continuous_won: {<VBP><VBN><VBG>+}
                Future Perfect Continuous: {<MD><VB|VBP><VBN><VBG>+}

                Future Perfect: {<MD><VB|VBP><VBN>+}
                Future Perfect: {<VBD><PRP><VBP><VBN>+}
                Future Perfect: {<MD><VB|VBP><VBN>+}

                Present Perfect Continuous: {<VBP|VBZ><VBN><VBG>+}

                Past Perfect Continuous: {<VBD|VBN><VBG>+}

                Present Perfect: {<VBP|VBZ><VBN>+}
                Present Perfect: {<VBP|VBZ><VBD|VBN>+}

                Past Perfect Continuous: {<VBD><VBN><VBG>+}
                Past Perfect: {<VBD|VBP><VBN|VBP>+}
               
                Future Simple: {<MD><VB>+}
                Future Simple: {<MD><VB|VBP|VBZ>+}
                
                Past Simple: {<VBD><TO><VB>}  
                Present Simple: {<VBP|VBZ><TO><VB>+}
                Present Simple: {<VBP|VBZ|VB>+}
                Past Simple: {<VBD|VBN>} 
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
        tokens_positions = list(WhitespaceTokenizer().span_tokenize(predl))  
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
        
        rt = text
        
        text1 = re.sub("must|have to|would|could|may|might|to have|could|can|shall", "", text)
        text1 = re.split(";|,|\n|-|:|and\s|for\s|but\s|or\s|yet\s|or\s|so\s|otherwise\s|while\s|else\s|for\s|whereas\s|if\s|that\s|\sas\s|because\s|what\s|whom\s|if\s|why\s|when\s|where\s|unless\s", text1)
        
        masive = []
        for i in range (len(text1)):
            if text1[i] == ' ':
                continue
            else:  
                result2 = self.def_tense(text1[i])
                if result2 != []:
                    masive.extend(result2)
        
        f1_r = masive
        f2_r = self.tok_pos(text)
        
        real_res = []
        
        for f1_r_e in f1_r:
            for f2_r_e in f2_r:
                if f1_r_e[0][0][0] in f2_r_e and f1_r_e[0][0][1] in f2_r_e:
                    real_res.append({'index': [*f2_r_e[:2]], 'tense': f1_r_e[0][1], 'target': f2_r_e[-1]})
                    
        for i in range(len(real_res)):
            new_indx = rt.find(real_res[i]['target'], real_res[i]['index'][0])
            if new_indx != -1:
                real_res[i]['index'] = [new_indx, new_indx + len(real_res[i]['target'])]
                
        real_real_res = []
        for x in real_res:
            found = False
            for y in real_real_res:
                if y['index'][0] == x['index'][0] and y['index'][1] == x['index'][1]:
                    found = True
                    break
            if not found:
                real_real_res.append(x)        
        
        real_real_res.sort(key=lambda x: x['index'][0])
        
        return real_real_res
        