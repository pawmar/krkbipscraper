# -*- coding: utf-8 -*-

import scrapy

BASE_URL = 'http://bip.krakow.pl'


class BipSpider(scrapy.Spider):
    name = 'bipspider'
    start_urls = ['http://bip.krakow.pl/index.php?bip_id=1&sw_id=-1&tab_id=2']

    def parse(self, response):
        for url in response.css('.kom_row a.float_lewy::attr("href")').extract():
            yield scrapy.Request(response.urljoin(url), self.parse_item)

    def parse_item(self, response):
        yield {
            'title': response.css('.news_title::text').extract(),
        }
