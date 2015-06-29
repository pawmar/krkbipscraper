# -*- coding: utf-8 -*-
"""Scrapy pipelines."""

import json
import codecs


class JsonWriterPipeline(object):

    def __init__(self):
        self.file = codecs.open('results.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
