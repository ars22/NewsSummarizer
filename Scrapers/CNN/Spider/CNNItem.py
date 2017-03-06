'''
Created on 07-Mar-2017

@author: Sri Ranga Sai
'''

import scrapy

class CNNItem(scrapy.item.Item):
    title = scrapy.Field(maxLength=100)
    text = scrapy.Field(default="")
    author = scrapy.Field(default="")
    keywords = scrapy.Field()
    link = scrapy.Field()
    
