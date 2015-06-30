# -*- coding: utf-8 -*-
"""Scraper for BIP announcements from bip.krakow.pl."""

import re
from datetime import datetime

import scrapy

from ..items import BipItem


HARD_LIMIT = 200


class BipSpider(scrapy.Spider):

    """Spider for Krakow's BIP."""

    name = 'bipspider'

    def __init__(self, limit=None, to_date=None):
        """Initial stuff.

        Keyword arguments (taken from scrapy command line):
        limit -- up to how many items to scrap
        to_date -- down to which date (format YYYY-MM-DD) scrap
                   the items

        If limit and to_date is set, limit has priority.
        """
        self.start_urls = [
            'http://bip.krakow.pl/index.php?bip_id=1&sw_id=-1&tab_id=2']
        if limit is None:
            self.limit = HARD_LIMIT
        else:
            self.limit = int(limit)
        self.to_date = to_date

    def parse(self, response):
        """Main scrapy parse function."""
        urls = response.css('.kom_row a.float_lewy::attr("href")').extract()
        for idx, url in enumerate(urls):
            if idx < self.limit:
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
