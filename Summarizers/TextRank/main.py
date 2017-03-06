'''
Created on 03-Mar-2017

@author: Sri Ranga Sai
'''
from os import listdir
from collections import Counter
from nltk.tokenize import sent_tokenize
from nltk.tokenize import wordpunct_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import os
import networkx as nx

class textrank:
    
    def __init__(self, doc):
    
        self.doc = doc
        self.text = self.doc.read()
        self.Puncts = ';\'",:-'
        self.CV = CountVectorizer() 
        
    def summarize(self):    
        
        self.sentences = sent_tokenize(self.text)
        
        self.tokenizedSentences = [] 
        for sentence in self.sentences:
            self.tokenizedSentences.append(Counter([word for word in wordpunct_tokenize(sentence) if word not in self.Puncts]))  
        
        self.b_matrix = self.CV.fit_transform(self.sentences)
        
        self.n_matrix = TfidfTransformer().fit_transform(self.b_matrix)
        
        self.sim_graph = self.n_matrix * self.n_matrix.T;
        
        self.sen_graph = nx.from_scipy_sparse_matrix(self.sim_graph)
        
        self.sen_scores = nx.pagerank(self.sen_graph)
        
        self.sorted_sentences_1 = sorted(self.sentences, key = lambda s: self.sen_scores[self.sentences.index(s)], reverse=True)
        
        self.sorted_sentences_2 = sorted(self.sorted_sentences_1[:5], key = lambda s: self.sentences.index(s))
        
    def textRankForSentence(self, sentence):
        pass
        
if __name__=='__main__':
    
    corpus_path = "C:/Users/Sri Ranga Sai/workspace/NewsSummarizer/Scrapers/NYT/Corpus"
    files = listdir(corpus_path)
    
    for doc in files[:1]:
        f = open(os.path.join(corpus_path, doc),'r')
        T = textrank(f)
        T.summarize()
        #print '\n\n'.join(T.sentences)
        print '\n\n'.join(T.sorted_sentences_2)