import scrapy
from scrapy.selector import Selector
import json
import os.path

class SoftJobSpider(scrapy.Spider):
    name = "softjob"
    base_url = 'https://www.ptt.cc'

    def __init__(self):
        self.page_count = 0

    def start_requests(self):
        url = 'https://www.ptt.cc/bbs/Soft_Job/index.html'
        yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_next_page(self, response):
        if self.page_count > 10: yield None
        self.page_count += 1
        url = self.base_url + response.css('.btn-group-paging a::attr(href)')[1].extract()
        yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_list(self, response):
        for x in response.css('.r-list-container div a::attr(href)'):
            url = self.base_url + x.extract()
            yield scrapy.Request(url=url, callback=self.save_page)
        yield scrapy.Request(url=response.url, callback=self.parse_next_page)

    def save_page(self, response):
        author, board, title, publish_datetime = response.css("#main-content span.article-meta-value::text").extract()
        result = {'author': author, 'board': board, 'title': title, 'publish_datetime': publish_datetime}

        content = []
        for x in response.css("#main-content::text, #main-content > div.push, #main-content > span.f2, #main-content span.f6").extract():
            if x.startswith('<div') and x.endswith('</div>'):
                sel = Selector(text=x)
                content += ["".join(sel.css('div.push > span::text').extract())]
            elif x.startswith('<span') and x.endswith('</span>'):
                sel = Selector(text=x)
                if sel.css('span.f6::text').extract():
                    content += [">> %s" % sel.css('span.f6::text').extract()[0]]
                else:
                    content += ["".join(sel.css('span.f2::text').extract())]
            else:
                content += [x]

        result.update({'url': response.url, 'content': content})
        yield result
