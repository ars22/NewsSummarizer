'''
Created on 25-Feb-2017

@author: Amrith
'''

import scrapy.cmdline
from Scrapers.NYT.Spider.NYItem import *
from scrapy.spiders import CrawlSpider
import re
import os

class NYSpider(CrawlSpider):
    
    name = "NYT"
    allowed_domains = ["nytimes.com"]
    start_urls = [
        "https://www.nytimes.com/2017/02/24/arts/desert-x-turns-an-arid-space-into-a-canvas.html"
    ]
    
    def parse(self, response):
        
        newsItem = NYItem()
        newsItem['title'] = uniToAscii(response.selector.xpath('//meta[@property="og:title"]/@content').extract_first())
        newsItem['author'] = uniToAscii(response.selector.xpath('//meta[@name="author"]/@content').extract_first())
        newsItem['link'] =  response.url
        
        print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n',newsItem['title']
        
        text = ""
        pars = response.selector.xpath('//*[@class="story-body-text story-content"]//text()').extract()
        for par in pars:
            par_text = uniToAscii(par)
            if par_text[-1:] != '.':
                par_text += '.'
            text = text + par_text + " "
        newsItem['text'] = text
       
        newsItem['keywords'] = uniToAscii(response.xpath("//meta[@name='news_keywords']/@content").extract_first())
        
        print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n',newsItem['title'],' ',len(pars),' ',newsItem['keywords']
        if newsItem['text']:
            print newsItem['text'][:100]
        
        yield newsItem
        
        storyLinks = response.selector.xpath("//a[@class='story-link']/@href").extract()
        
        for link in storyLinks:
            if re.match('https://www.nytimes.com/2017/02/2.*\.html', str(link)):
                pass
                #print 'Fetching from ',str(link)
                #yield scrapy.Request(str(link))
            
    
def uniToAscii(text):
    
    if text is None:
        return text
    
    uni2ascii = {
            ord('\xe2\x80\x99'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\x9c'.decode('utf-8')): ord('"'),
            ord('\xe2\x80\x9d'.decode('utf-8')): ord('"'),
            ord('\xe2\x80\x9e'.decode('utf-8')): ord('"'),
            ord('\xe2\x80\x9f'.decode('utf-8')): ord('"'),
            ord('\xc3\xa9'.decode('utf-8')): ord('e'),
            ord('\xe2\x80\x9c'.decode('utf-8')): ord('"'),
            ord('\xe2\x80\x93'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x92'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x94'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x94'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x98'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\x9b'.decode('utf-8')): ord("'"),

            ord('\xe2\x80\x90'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x91'.decode('utf-8')): ord('-'),

            ord('\xe2\x80\xb2'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb3'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb4'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb5'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb6'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb7'.decode('utf-8')): ord("'"),

            ord('\xe2\x81\xba'.decode('utf-8')): ord("+"),
            ord('\xe2\x81\xbb'.decode('utf-8')): ord("-"),
            ord('\xe2\x81\xbc'.decode('utf-8')): ord("="),
            ord('\xe2\x81\xbd'.decode('utf-8')): ord("("),
            ord('\xe2\x81\xbe'.decode('utf-8')): ord(")"),
            ord('\xe2\x80\x95'.decode('utf-8')): ord("-")
            }
    
    return text.translate(uni2ascii).encode('ascii','ignore')
    
def main():
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'Scrapers.NYT.Spider.settings';
    scrapy.cmdline.execute(argv=['scrapy', 'runspider', 'NYSpider.py'])
    
if __name__ == '__main__':
    main()
            
            