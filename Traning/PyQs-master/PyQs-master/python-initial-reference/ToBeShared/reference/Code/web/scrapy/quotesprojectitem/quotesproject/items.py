# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst,Compose,Identity

class QuotesprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
    

class QuotesprojectItemWithProcessor(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    text = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst(),
        )
    author = scrapy.Field(input_processor=Identity(),
        output_processor=TakeFirst(),
        )
    tags = scrapy.Field(input_processor=Identity(),
        output_processor=Identity(),
        )