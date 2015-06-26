# -*- coding: utf-8 -*-
"""Scraper for BIP announcements from bip.krakow.pl."""

import re
from datetime import datetime

import scrapy


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
        metadata = self._parse_metadata(response)
        item = {
            'id': re.findall('news_id=(\d+)', response.url)[0],
            'title': self._parse_title(response),
        }
        item.update(metadata)
        yield self._encode_item(item)

    def _parse_title(self, response):
        """Get announcement title from response."""
        title = response.css('.news_title::text').extract_first()
        if not title:
            title = response.css('.news_title a::text').extract_first()
        return title

    def _parse_metadata(self, response):
        """Extract metadata from item footer."""
        date_fields = [
            'date_created',
            'date_published',
            'date_edited',
        ]
        data = {}
        footer = response.css('#bipLabel em')
        data['publisher_org'] = footer[0].css('a::text').extract_first()
        data['publisher_org_link'] = footer[0] \
            .css('a::attr("href")').extract_first()
        person_responsible_text = footer[1].css('em::text').extract_first()
        data['person_responsible'], data['person_responsible_title'] = \
            person_responsible_text.split(' - ')
        data['person_publisher'] = footer[2].css('em::text').extract_first()
        for i, fitem in enumerate(footer[3:]):
            data[date_fields[i]] = datetime.strptime(
                fitem.css('em::text').extract_first(),
                '%Y-%m-%d'
                ).date()
        return data

    def _encode_item(self, item, enc='utf-8'):
        """Encode text fields in item."""
        fields = ('title', 'publisher_org', 'person_responsible',
                  'person_responsible_title', 'person_publisher')
        for field in fields:
            item[field] = item[field].encode(enc)
        return item
