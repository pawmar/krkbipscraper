# -*- coding: utf-8 -*-
"""Scrapy settings."""

BOT_NAME = 'krkbipscraper'

SPIDER_MODULES = ['krkbipscraper.spiders']
NEWSPIDER_MODULE = 'krkbipscraper.spiders'

ITEM_PIPELINES = ['krkbipscraper.pipelines.JsonWriterPipeline']
