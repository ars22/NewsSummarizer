'''
Created on 06-Mar-2017

@author: Sri Ranga Sai
'''

import nltk
import nltk.data
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import operator
import math

DEBUG = True

TARGET_ARTICLE_PATH = 'C:/Users/Sri Ranga Sai/workspace/NewsSummarizer/Scrapers/NYT/Corpus/\'Desert X\' Treats Arid Space as a Rich Canvas'
NUM_NP = 10
K = 10
stopword_list = stopwords.words('english')

def read_article(path):
    fp = open(path)
    lines = fp.readlines()

    body = ""

    for line in lines:
        body += line.rstrip('\n') + " "

    return  body

def preprocess(body):
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')    

    body = sent_tokenizer.tokenize(body)
    body = [word_tokenize(sent) for sent in body]
    body = [nltk.pos_tag(sent) for sent in body]
    
    return body

def acceptable_phrase(phrase):
    l = [word for word in phrase.split() if word not in stopword_list and len(word) > 3]
    return len(l) > 0

def cleaned_phrase(phrase):
    cleaned = ""
    for word in phrase.split():
        if acceptable_phrase(word):
            cleaned = word + " "
    cleaned = cleaned.strip()
    return cleaned
    
def get_score(keyphrases, freq_phrases, freq_words):
    score = 0
    for phrase in freq_phrases.items():
        for keyphrase in keyphrases:
            if phrase[0] == keyphrase[0]:
                score += keyphrase[1] * math.sqrt(phrase[1])
                break
                
    for word in freq_words.items():
        for keyphrase in keyphrases:
            if word[0] == keyphrase[0]:
                score += keyphrase[1] * math.sqrt(word[1])
                break
    # if DEBUG:
    #     print freq_phrases, ' | ', freq_words, ' | ', score            
    return score

def leaves_NP(tree):
    for subtree in tree.subtrees(filter = lambda t: t.node=='NP'):
        yield subtree.leaves()
        
def summarize(body):

    body_pos = preprocess(body)
        
    # grammar = "NP: {<DT>?<JJ>*<NN>}"
    grammar = r"""
    NBAR:
    {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
    
    NP:
    {<DT>?<JJ>*<NN>}
    {<NBAR>}
    {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
    """
    chunker = nltk.RegexpParser(grammar)
    trees = [chunker.parse(sent) for sent in body_pos]
    
    print body_pos[:5]
    
    NP = {}
    cnt = 0
    for tree in trees:
        for leaf_NP in leaves_NP(tree):
            
            phrase = ""
            for word in leaf_NP:
                phrase += str(word[0]).lower() + " "
            print '%%%%%%%%%%%%%%%%%%%%%%%%%%\n',phrase
            phrase = phrase.strip()
            print '%%%%%%%%%%%%%%%%%%%%%%%%%%\n',phrase
            phrase = cleaned_phrase(phrase)
            print '%%%%%%%%%%%%%%%%%%%%%%%%%%\n',phrase
            
            if phrase in NP:
                NP[phrase] += 1
            elif acceptable_phrase(phrase):
                NP[phrase] = 1
            
            if len(phrase.split()) > 1:
                for word in phrase.split():
                    if word in NP:
                        NP[word] += 1.0 / len(phrase.split())
                    elif acceptable_phrase(word):
                        NP[word] = 1.0 / len(phrase.split())
                        
    keyphrases = sorted(NP.items(), key=operator.itemgetter(1), reverse = True)[0 : NUM_NP+1]
    keyphrases = [(phrase[0], float(phrase[1]) / len(NP)) for phrase in keyphrases]
    if DEBUG:
        print keyphrases, '\n'
    
    scores_dict = {}
    sent_score = [0.0 for x in trees]
    for i, tree in enumerate(trees):
        score = 0
        freq_phrases = {}
        freq_words = {}
        for leaf_NP in leaves_NP(tree):
            phrase = ""
            for word in leaf_NP:
                phrase += str(word[0]).lower() + " "
            phrase = phrase.strip()
            phrase = cleaned_phrase(phrase)
            
            if phrase in freq_phrases:
                freq_phrases[phrase] += 1
            elif acceptable_phrase(phrase):
                freq_phrases[phrase] = 1
                
            if len(phrase.split()) > 1:
                for word in phrase.split():
                    if word in freq_words:
                        freq_words[word] += 1
                    elif acceptable_phrase(word):
                        freq_words[word] = 1
        score = get_score(keyphrases, freq_phrases, freq_words)
        scores_dict[i] = score
        sent_score[i] = score
        
    if len(body_pos)/3>10:
        K = 10
    else:
        K = len(body_pos)/3
    K = K+1
    scores = sorted(scores_dict.items(), key=operator.itemgetter(1), reverse = True)[0 : K + 1]

    # contains_first = True if len([score for score in scores if score[0] == 0]) > 0 else False
    # if DEBUG:
    #     print 'contains first: ', contains_first
    #     #print scores_dict
    # if not contains_first:
    #     if DEBUG:
    #         print 'setting score for sent 0 = score for sent ', scores[K][0], ' = ', scores[K][1], ' (orig score for sent 0 =  ', scores_dict[0], ')'
    #     sent_score[0] = scores[K][1]
    #     scores_dict[0] = scores[K][1]    
    #     scores[K] = (0, scores[K][1])
        
    scores = sorted(scores, key = operator.itemgetter(0))

    if DEBUG:
        print '\n', scores, '\n'
        
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    body_sent = sent_tokenizer.tokenize(body)
    summary = []
    if scores[0][0] != 0:
        summary.append((body_sent[0], 0, scores_dict[0]))
    for score in scores:
        summary.append((body_sent[score[0]], score[0], score[1]))
    if DEBUG:
        print "Keyphrase"
        for line in summary:
            print line                   
    #return summary
    sentences = sent_tokenizer.tokenize(body)
    #return sent_score
    return [(sentences[i], scores_dict[i]) for i in xrange(len(sentences))]
    
def main():
    
    body = read_article(TARGET_ARTICLE_PATH)

    summary = summarize(body)
    
    print summary
    # print '\n'                   
    # for line in summary:
    #     print line, '\n'

if DEBUG:
    main()