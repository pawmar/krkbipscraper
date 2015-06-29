# -*- coding: utf-8 -*-
"""Scraper for BIP announcements from bip.krakow.pl."""

import re
from datetime import datetime

import scrapy

from ..items import BipItem


class BipSpider(scrapy.Spider):

    """Spider for Krakow's BIP."""

    name = 'bipspider'
    start_urls = ['http://bip.krakow.pl/index.php?bip_id=1&sw_id=-1&tab_id=2']

    def parse(self, response):
        """Main scrapy parse function."""
        limit = 5
        urls = response.css('.kom_row a.float_lewy::attr("href")').extract()
        for idx, url in enumerate(urls):
            if idx < limit:
                yield scrapy.Request(response.urljoin(url), self.parse_item)

    def parse_item(self, response):
        """Extract single announcement data."""
        item = BipItem()
        item['id'] = re.findall('news_id=(\d+)', response.url)[0]
        item['title'] = self._parse_title(response)
        item = self._parse_metadata(response, item)
        yield item

    def _parse_title(self, response):
        """Get announcement title from response."""
        title = response.css('.news_title::text').extract_first()
        if not title:
            title = response.css('.news_title a::text').extract_first()
        return title

    def _parse_metadata(self, response, item):
        """Extract metadata from item footer."""
        date_fields = [
            'date_created',
            'date_published',
            'date_edited',
        ]
        footer = response.css('#bipLabel em')
        item['publisher_org'] = footer[0].css('a::text').extract_first()
        item['publisher_org_link'] = footer[0] \
            .css('a::attr("href")').extract_first()
        person_responsible_text = footer[1].css('em::text').extract_first()
        item['person_responsible'], item['person_responsible_title'] = \
            person_responsible_text.split(' - ')
        item['person_publisher'] = footer[2].css('em::text').extract_first()
        for i, fitem in enumerate(footer[3:]):
            item[date_fields[i]] = fitem.css('em::text').extract_first()
        return item
