# -*- coding: utf-8 -*-
import scrapy
from quotesproject.items import QuotesprojectItem

class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'toscrape-xpath'
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    def parse(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        for quote in response.xpath('//div[@class="quote"]'):            
            item = QuotesprojectItem()
            item['text'] = quote.xpath('./span[@class="text"]/text()').extract_first()
            item['author'] = quote.xpath('.//small[@class="author"]/text()').extract_first()
            item['tags'] = quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract()
            yield item

        next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url),callback=self.parse)


