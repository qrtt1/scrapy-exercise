import scrapy
from scrapy.selector import Selector
import json
import os.path

class SoftJobSpider(scrapy.Spider):
    name = "softjob"
    base_url = 'https://www.ptt.cc'
    skip_page_uris = ['/bbs/Soft_Job/index1.html', '/bbs/Soft_Job/index.html']

    def start_requests(self):
        url = 'https://www.ptt.cc/bbs/Soft_Job/index.html'
        request = scrapy.Request(url=url, callback=self.parse_next_page)
        request.meta['page'] = 0
        yield request

    def parse_next_page(self, response):
        yield response.follow(response.url, self.parse_list)
        for url in response.css('.btn-group-paging a::attr(href)').extract():
            yield response.follow(url, self.parse_list)
            if url in self.skip_page_uris: continue
            next_page_url = self.base_url + url
            print "next_page_url", next_page_url
            request = scrapy.Request(url=next_page_url, callback=self.parse_next_page)
            if 'page' not in response.meta:
                request.meta['page'] = 0
            else:
                request.meta['page'] = response.meta['page'] + 1

            if request.meta['page'] <= 5:
                yield request

    def parse_list(self, response):
        print "parse_list", response.url
        for x in response.css('.r-list-container div a::attr(href)'):
            yield response.follow(x, self.save_page)

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
