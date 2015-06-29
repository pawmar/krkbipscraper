# -*- coding: utf-8 -*-
"""Scapy items."""

import scrapy


class BipItem(scrapy.Item):

    """Bip announcement item."""

    id = scrapy.Field()
    title = scrapy.Field()
    publisher_org = scrapy.Field()
    publisher_org_link = scrapy.Field()
    person_responsible = scrapy.Field()
    person_responsible_title = scrapy.Field()
    person_publisher = scrapy.Field()
    date_created = scrapy.Field()
    date_published = scrapy.Field()
    date_edited = scrapy.Field()
