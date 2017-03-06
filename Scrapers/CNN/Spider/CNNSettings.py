'''
Created on 07-Mar-2017

@author: Sri Ranga Sai
'''
import sys
import os
from os.path import dirname

path = dirname(dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(path)

SPIDER_MODULES = ['Scrapers.CNN.Spider']
NEWSPIDER_MODULE = 'Scrapers.CNN.Spider'

BOT_NAME = 'cnn_scraper'

ITEM_PIPELINES = {
    'Scrapers.CNN.Spider.CNNPipeline.Pipeline1': 300,
    'Scrapers.CNN.Spider.CNNPipeline.Pipeline2': 800
}

