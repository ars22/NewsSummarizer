'''
Created on 25-Feb-2017

@author: Sri Ranga Sai
'''
from scrapy.exceptions import DropItem

class NYPipeline1(object):
    
    def process_item(self, item, spider):
        try:
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ IN NY1 : ',item['title']
            if item['text']!='':
                return item
            else:
                raise DropItem('Item with no text Dropped')
        except DropItem:
            print('Item with no text')