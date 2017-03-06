'''
Created on 25-Feb-2017

@author: Sri Ranga Sai
'''

import os

class NYPipeline2(object):
    
    def process_item(self, item, spider):
        if item is not None:
            print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ IN NY2 : ',item['title']
            print '%%%%%%%%%%%%%%%%%%',os.path.join(os.path.abspath(os.curdir),'/NewsSummarizer/Scrapers/NYT/Corpus/'+item['title'])
            with open('C:/Users/Sri Ranga Sai/workspace/NewsSummarizer/Scrapers/NYT/Corpus/'+self.process(item['title']),'w') as f:
                f.write(item['text'])
                f.close()

    def process(self, st):
        if (st.find(':')>0):
            return st[:st.find(':')]
        else:
            return st