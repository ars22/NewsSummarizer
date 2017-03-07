'''
Created on 07-Mar-2017

@author: Sri Ranga Sai
'''

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords 
from nltk.tag import pos_tag
import nltk.data
import json 
import nltk
import numpy as np
import os
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from os import listdir

class WordNet:
    
    def __init__(self, corpus):
        self.corpus = corpus
        self.grammar = """
             NP: {<DT|PP\$>?<JJ>*<NN>}   
            {<NNP>+}    
            {<NBAR>}
            {<NBAR><IN><NBAR>}
            
            NBAR:
            {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
                
        """
        self.chunker = nltk.RegexpParser(self.grammar)
        
    def read_corpus(self):
        for fd in self.corpus:
            item = self.read_file(fd)
            #print 'Generating summary for ',item['title']
            #self.generate_summary(item['text'])
            self.generate_summary(item)
            
    def read_file(self, f):
        #item = json.loads(f.read())
        item = f.read()
        return item
    
    def process_text(self, text):
        #nltk.download()
        #sent_tokenizer = nltk.data.load('tokenizers/punkt/data/english.pickle')
        #text = sent_tokenizer.tokenize(text)
        text = sent_tokenize(text)
        text = [word_tokenize(sen) for sen in text]
        text = [pos_tag(sen) for sen in text]
        
    def generate_summary(self, text):
        
        text = self.process_text(text)
        
        print text
        popular_noun_phrases = {}
        keywords = {}
        
        for sen in text:

            tree = self.chunker.parse(sen)             
            
            NP = self.noun_phrases(tree)
            
            total_phrase = ""
                        
            for noun in NP:
                X = noun.lower().strip()
                if self.accept(X):
                    total_phrase += X

            if (total_phrase in popular_noun_phrases):
                popular_noun_phrases[total_phrase] += 1
            else:
                popular_noun_phrases[total_phrase] = 1
                
        
        print '\n'.join(popular_noun_phrases)
        
        for phrase in popular_noun_phrases:
            for word in phrase.split():
                if (word in keywords[word]): 
                    keywords[word] +=1
                else:
                    keywords[word] = 1
            
        
        CV = CountVectorizer()
        b_matrix = CV.fit_transform([phrase for phrase,val in popular_noun_phrases.items()])
        b_matrix = TfidfTransformer.fit_transform(b_matrix)
        phrase_graph = np.dot(b_matrix , b_matrix.T)
        for i in b_matrix.size()[0]:
            for j in b_matrix.size()[1]:
                S1 = np.dot(b_matrix[i], b_matrix[i].T)
                S2 = np.dot(b_matrix[i], b_matrix[i].T)
                phrase_graph[i][j]/=(S1 * S2)
        
        print popular_noun_phrases
        print keywords               
        
    def noun_phrases(self, T):
        for stree in T.subtrees(filter = lambda t: t.node()=='NP'):
            yield stree.leaves()
            
    def accept(self, word):
        X = word.lower().strip()
        if (X in stopwords and len(X)>3):
            return True
        return False
            
        
def main():
    corpus_path = 'C:/Users/Sri Ranga Sai/workspace/NewsSummarizer/Scrapers/NYT/Corpus'
    corpus = [open(os.path.join(corpus_path,fname),'r') for fname in listdir(corpus_path)]
    W = WordNet(corpus)
    W.read_corpus()
    
if __name__ == '__main__':
    main()