'''
Created on 07-Mar-2017

@author: Sri Ranga Sai
'''

from scrapy.exceptions import DropItem
import os
import json

class Pipeline1(object):
    
    def process_item(self, item, spider):
        try:
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ IN CNN1 : ',item['title']
            if item['text']!='':
                return item
            else:
                raise DropItem('Item with no text Dropped')
        except DropItem:
            print('Item with no text')
            
            
class Pipeline2(object):
    
    def process_item(self, item, spider):
        if item is not None:
            print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ IN CNN2 : ',item['title']
            print '%%%%%%%%%%%%%%%%%%',os.path.join(os.path.abspath(os.curdir),'/NewsSummarizer/Scrapers/CNN/Corpus/'+item['title'])
            with open('C:/Users/Sri Ranga Sai/workspace/NewsSummarizer/Scrapers/CNN/Corpus/'+self.process(item['title']),'w') as f:
                f.write(json.dumps(item))
                f.close()

    def process(self, st):
        if (st.find(':')>0):
            return st[:st.find(':')]
        else:
            return st