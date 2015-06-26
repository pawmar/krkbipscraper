# -*- coding: utf-8 -*-
"""Scraper for BIP announcements from bip.krakow.pl."""

import re

import scrapy

BASE_URL = 'http://bip.krakow.pl'


class BipSpider(scrapy.Spider):

    """Spider for Krakow's BIP."""

    name = 'bipspider'
    start_urls = ['http://bip.krakow.pl/index.php?bip_id=1&sw_id=-1&tab_id=2']

    def parse(self, response):
        """Main scrapy parse function."""
        for url in response.css('.kom_row a.float_lewy::attr("href")') \
                           .extract():
            yield scrapy.Request(response.urljoin(url), self.parse_item)

    def parse_item(self, response):
        """Extract single announcement data."""
        yield {
            'id': re.findall('news_id=(\d+)', response.url)[0],
            'title': response.css('.news_title::text').extract()[0],
        }
