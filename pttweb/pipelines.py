# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import os
import os.path
from scrapy.exceptions import DropItem
import json
import codecs


class TutorialPipeline(object):
    def process_item(self, item, spider):
        if 'board' not in item:
            raise DropItem('missing board name')
        if 'url' not in item:
            raise DropItem('missing url')

        base_dir = os.path.join(spider.local_storage_path, item['board'])
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        if 'text' in item:
            filename = item['url'].split("/")[-1] + ".txt"
            with codecs.open(os.path.join(base_dir, filename), "w", "utf-8") as fh:
                fh.write(item['text'])
        return item
