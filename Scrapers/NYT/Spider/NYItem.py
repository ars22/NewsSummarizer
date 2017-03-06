'''
Created on 25-Feb-2017

@author: Amrith
'''


import scrapy

class NYItem(scrapy.item.Item):
    title = scrapy.Field(maxLength=100)
    text = scrapy.Field(default="")
    author = scrapy.Field(default="")
    keywords = scrapy.Field()
    link = scrapy.Field()
    