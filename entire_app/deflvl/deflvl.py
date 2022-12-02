import re
import pandas as pd
#import en_core_web_sm
import numpy as np
import spacy
import pickle
import gensim.downloader
from nltk.tokenize import RegexpTokenizer
from catboost import CatBoostClassifier

import pathlib

class DefineLevelApp:
    def __init__(self):
        pass
    
    def init_app(self):
        with pathlib.Path('deflvl/CBClf.pkl').open('rb') as file:
            self.clf = pickle.load(file)
        self.sp = spacy.load('en_core_web_sm')
        self.w2vm = gensim.downloader.load('word2vec-google-news-300')
        print('DefineLevelApp: initialized')
        
    def preprocess_text(self, text):
        text = self.simplify_punctuation(text)
        text = self.lemmatization_del_sw(text)
        text = re.sub(r'([^a-zA-Z\\n]+)', ' ', text)
        return text
        
    def lemmatization_del_sw(self, text):
        doc = self.sp(text)
        lemmatized_output = ' '.join([str(token.lemma_) for token in doc])
        return lemmatized_output
        
    def simplify_punctuation(self, text):
        text = re.sub(r'([^a-zA-Z\'\\n]+)', ' ', text)
        text = re.sub(r"^\s+", "", text)
        text = re.sub(r"[ ]*(\n|\r\n|\r)[ ]*", " ", text)
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\s+$", "", text)
        return text
        
    def get_average_word2vec(self, tokens_list, vector, generate_missing=False, k=300):
        if len(tokens_list)<1:
            return np.zeros(k)
        if generate_missing:
            vectorized = [vector[word] if word in vector else np.random.rand(k) for word in tokens_list]
        else:
            vectorized = [vector[word] if word in vector else np.zeros(k) for word in tokens_list]
        length = len(vectorized)
        summed = np.sum(vectorized, axis=0)
        averaged = np.divide(summed, length)
        return averaged

    def get_word2vec_embeddings(self, vectors, clean_questions, generate_missing=False):
        embeddings = self.get_average_word2vec(clean_questions, vectors, generate_missing=generate_missing)
        return list(embeddings)
        
        
    def define_level(self, text):
        ptext = self.preprocess_text(text)
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(text)
        embeddings = self.get_word2vec_embeddings(self.w2vm, tokens)
        y_pred = self.clf.predict(embeddings)
        CEFR = {0: 'A2', 1: 'B1', 2: 'B2', 3: 'C1'}
        ans = CEFR[int(y_pred)]
        return ans
        
    def define_test(self, text):
        return 'A1'