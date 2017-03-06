'''
Created on 25-Feb-2017

@author: Sri Ranga Sai
'''

#This is the config file for the Ney York Times Spider settings
import sys
import os
from os.path import dirname

path = dirname(dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(path)

SPIDER_MODULES = ['Scrapers.NYT.Spider']
NEWSPIDER_MODULE = 'Scrapers.NYT.Spider'

BOT_NAME = 'nyt_scraper'

ITEM_PIPELINES = {
    'Scrapers.NYT.Spider.NYPipeline1.NYPipeline1': 300,
    'Scrapers.NYT.Spider.NYPipeline2.NYPipeline2': 800
}

