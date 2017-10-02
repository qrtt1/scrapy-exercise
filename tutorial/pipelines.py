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
        if not os.path.exists(item['board']): os.makedirs(item['board'])

        filename = item['url'].split("/")[-1] + ".json"
        with codecs.open(os.path.join(item['board'], filename), "w") as fh:
            fh.write(json.dumps(item, indent=4, sort_keys=True))
        return item
