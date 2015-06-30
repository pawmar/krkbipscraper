# -*- coding: utf-8 -*-
"""Scraper for BIP announcements from bip.krakow.pl."""

import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.exceptions import CloseSpider

from ..items import BipItem


HARD_LIMIT = 200


class BipSpider(CrawlSpider):

    """Spider for Krakow's BIP."""

    name = 'bipspider'
    start_urls = [
        'http://bip.krakow.pl/index.php?bip_id=1&sw_id=-1&tab_id=2']
    rules = [
        Rule(LinkExtractor(
            restrict_xpaths='//div[@class="srodek"]/'
                            'a[contains(text(), "Dalej")]')),
        Rule(LinkExtractor(
                 restrict_css='.kom_row a.float_lewy'),
             callback='parse_item'),
    ]

    def __init__(self, *args, **kwargs):
        """Initial stuff.

        Keyword arguments (taken from scrapy command line):
        limit -- up to how many items to scrap
        to_date -- down to which date (format YYYY-MM-DD) scrap
                   the items

        If limit and to_date is set, limit has priority.
        """
        super(BipSpider, self).__init__(*args, **kwargs)
        self.num_parsed = 0
        limit = kwargs.get('limit')
        to_date = kwargs.get('to_date')
        if limit is None:
            self.limit = HARD_LIMIT
        else:
            self.limit = int(limit)
        self.to_date = to_date

    # def parse(self, response):
    #     """Main scrapy parse function."""
    #     urls = response.css('.kom_row a.float_lewy::attr("href")').extract()
    #     for idx, url in enumerate(urls):
    #         if idx < self.limit:
    #             yield scrapy.Request(response.urljoin(url), self.parse_item)

    def parse_item(self, response):
        """Extract single announcement data."""
        if self.num_parsed > self.limit:
            raise CloseSpider("Limit of %d items reached" % self.limit)
        item = BipItem()
        item['id'] = re.findall('news_id=(\d+)', response.url)[0]
        item['title'] = self._parse_title(response)
        item = self._parse_metadata(response, item)
        self.num_parsed += 1
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
