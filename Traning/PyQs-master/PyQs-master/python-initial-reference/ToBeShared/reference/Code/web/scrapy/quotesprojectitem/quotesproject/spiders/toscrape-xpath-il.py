# -*- coding: utf-8 -*-
import scrapy
from quotesproject.items import QuotesprojectItemWithProcessor
from scrapy.loader import ItemLoader



class ToScrapeSpiderXPathItemLoader(scrapy.Spider):
    name = 'toscrape-xpath-il'
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            nl = ItemLoader(item=QuotesprojectItemWithProcessor(), selector=quote)
            nl.add_xpath('text', './span[@class="text"]/text()')
            nl.add_xpath('author', './/small[@class="author"]/text()')
            nl.add_xpath('tags', './/div[@class="tags"]/a[@class="tag"]/text()')                  
            yield nl.load_item()

        next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url),callback=self.parse)


